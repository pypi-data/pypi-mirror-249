# SPDX-License-Identifier: MIT

from pathlib import Path
import configparser
import getpass

from click import ClickException, echo

import requests

DIST_GIT = "src.fedoraproject.org"
DIST_GIT_URL = f"https://{DIST_GIT}/api/0/"
BZOVERRIDES_URL = f"https://{DIST_GIT}/_dg/bzoverrides/"

ANITYA_URL = "https://release-monitoring.org/api/v2/"


class OnboarderException(ClickException):
    pass


class Onboarder:
    def __init__(self, config):
        if config is not None and Path(config).exists():
            self.config = configparser.ConfigParser()
            self.config.read(config)
        else:
            raise OnboarderException(f"Invalid or missing config: {config}")

        try:
            api_config = self.config["api"]
            self.anitya_token = api_config["anitya_token"]
            self.dist_git_token = api_config.get("dist_git_token", None)
            self.username = api_config.get("username", None)
        except KeyError:
            raise OnboarderException(f"anitya_token not defined in {config}") from None

        # Fallback to fedpkg_config is dist_git_token is not defined in the config.
        fedpkg_config_path = Path.home() / ".config/rpkg/fedpkg.conf"
        if self.dist_git_token is None and fedpkg_config_path.exists():
            try:
                echo(
                    f"api.dist_git_token is not defined in {config}. "
                    + "Falling back to fedpkg config file"
                )
                self.fedpkg_config = configparser.ConfigParser()
                self.fedpkg_config.read(fedpkg_config_path)
                self.dist_git_token = self.fedpkg_config.get("fedpkg.distgit", "token")
            except (configparser.NoSectionError, configparser.NoOptionError):
                raise OnboarderException(
                    f"A distgit token was not found in {config} or {fedpkg_config_path}"
                ) from None

        # Fail if dist_git_token was not defined in either of the two places
        if getattr(self, "dist_git_token", None) is None:
            raise OnboarderException(f"api.dist_git_token not defined in {config}")

        # Fallback if username is not defined
        if self.username is None:
            fedora_upn_path = Path.home() / ".fedora.upn"
            if fedora_upn_path.exists():
                with open(fedora_upn_path, "r") as f:
                    self.username = f.read().strip()
            else:
                self.username = getpass.getuser()

    def get_anitya_project(self, package, ecosystem=None):
        project = package
        if not ecosystem:
            if package.startswith("python-"):
                project = package.split("-", 1)[1]
                ecosystem = "pypi"
            elif package.startswith("rust-"):
                project = package.split("-", 1)[1]
                ecosystem = "crates.io"
            else:
                raise OnboarderException(f"Could not determine ecosystem for {package}")

        url = requests.compat.urljoin(ANITYA_URL, "projects/")
        get_data = {"ecosystem": ecosystem, "name": project}
        req = requests.get(url, get_data)
        json = req.json()
        if json["total_items"] == 1:
            return json["items"][0]
        else:
            return None

    def get_anitya_package(self, package, distribution="Fedora"):
        url = requests.compat.urljoin(ANITYA_URL, "packages/")
        get_data = {"distribution": distribution, "name": package}
        req = requests.get(url, get_data)
        json = req.json()
        if json["total_items"] == 1:
            return json["items"][0]
        else:
            return None

    def get_package_info(self, package):
        url = requests.compat.urljoin(DIST_GIT_URL, f"rpms/{package}")
        req = requests.get(url)
        json = req.json()
        if "name" in json:
            return json
        else:
            return None

    def add_anitya_project(self, package, ecosystem=None, homepage=None):
        project = package
        if not ecosystem:
            if package.startswith("python-"):
                project = package.split("-", 1)[1]
                ecosystem = "pypi"
                if not homepage:
                    homepage = f"https://pypi.org/project/{project}"
            elif package.startswith("rust-"):
                project = package.split("-", 1)[1]
                ecosystem = "crates.io"
                if not homepage:
                    homepage = f"https://crates.io/crates/{project}"
        url = requests.compat.urljoin(ANITYA_URL, "projects/")
        post_data = {
            "name": project,
            "backend": ecosystem,
            "homepage": homepage,
        }
        req = requests.post(
            url, post_data, headers={"Authorization": f"token {self.anitya_token}"}
        )
        req.raise_for_status()
        return req.json()

    def set_anitya_version(self, project_id):
        url = requests.compat.urljoin(ANITYA_URL, "versions/")
        post_data = {
            "id": project_id,
            "version_scheme": "Semantic",
            "version_filter": "alpha;beta;rc;pre",
            "dry_run": False,
        }
        req = requests.post(
            url, post_data, headers={"Authorization": f"token {self.anitya_token}"}
        )
        req.raise_for_status()
        return req.json()

    def add_anitya_package(
        self, package, project, ecosystem=None, distribution="Fedora"
    ):
        if not ecosystem:
            if package.startswith("python-"):
                project = package.split("-", 1)[1]
                ecosystem = "pypi"
            elif package.startswith("rust-"):
                project = package.split("-", 1)[1]
                ecosystem = "crates.io"
        url = requests.compat.urljoin(ANITYA_URL, "packages/")
        post_data = {
            "distribution": distribution,
            "package_name": package,
            "project_name": project,
            "project_ecosystem": ecosystem,
        }
        req = requests.post(
            url, post_data, headers={"Authorization": f"token {self.anitya_token}"}
        )
        req.raise_for_status()
        return req.json()

    def add_package_acl(self, package, group, acl):
        url = requests.compat.urljoin(DIST_GIT_URL, f"rpms/{package}/git/modifyacls")
        post_data = {"user_type": "group", "name": group, "acl": acl}
        req = requests.post(
            url, post_data, headers={"Authorization": f"token {self.dist_git_token}"}
        )
        req.raise_for_status()
        return req.json()

    def set_bugzilla_assignee(self, package, group):
        url = requests.compat.urljoin(BZOVERRIDES_URL, f"rpms/{package}")
        post_data = {"epel_assignee": f"@{group}", "fedora_assignee": f"@{group}"}
        req = requests.post(
            url, post_data, headers={"Authorization": f"token {self.dist_git_token}"}
        )
        req.raise_for_status()
        return req.json()

    def add_package_to_anitya(self, package, ecosystem=None):
        project = self.get_anitya_project(package, ecosystem)
        if not project:
            out = self.add_anitya_project(package, ecosystem)
            project = self.get_anitya_project(package, ecosystem)
            if not project:
                raise OnboarderException(f"Adding project failed: {out}")
        project_id = project["id"]
        if package.startswith("rust-"):
            self.set_anitya_version(project_id)
        if not self.get_anitya_package(package):
            self.add_anitya_package(package, project["name"], ecosystem)

    def get_packages(self, pattern):
        url = requests.compat.urljoin(DIST_GIT_URL, f"projects")
        current_page = 1
        projects = []
        while True:
            get_data = {
                "owner": self.username,
                "pattern": pattern,
                "per_page": 100,
                "page": current_page,
            }
            req = requests.get(
                url, get_data, headers={"Authorization": f"token {self.dist_git_token}"}
            )
            req.raise_for_status()
            result = req.json()
            projects += result["projects"]
            pages = result["pagination"]["pages"]
            if current_page == pages:
                break
            else:
                current_page += 1

        packages = []
        for p in projects:
            # Pagination can result in duplicates
            is_duplicate = False
            for pkg in packages:
                if p["name"] == pkg["name"]:
                    is_duplicate = True

            if is_duplicate:
                continue

            # The API sometimes returns extra packages, we just want ours
            if p["access_users"]["owner"] == [self.username]:
                packages.append(p)

        return packages
