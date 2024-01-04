# fedora-sig-onboard

`fedora-sig-onboard` is a simple tool to onboard a Fedora package onto the relevant SIG. It will attempt to add the SIG to the package ACL, update the Bugzilla assignee and add the package to [Anitya](https://release-monitoring.org). Rust and Golang packages are currently supported, and will be respectively onboarded onto the [Rust SIG](https://fedoraproject.org/wiki/SIGs/Rust) and the [Go SIG](https://fedoraproject.org/wiki/SIGs/Go).

# Installation

On Fedora Linux 38 or later:

``` console
dnf install fedora-sig-onboard
```

otherwise

``` console
pip install 'git+https://pagure.io/fedora-sig-onboard.git'
```

## Usage

Add your dist-git and Anitya to the configuration file in `~/.config/fedora-sig-onboard/fedora-sig-onboard.conf`:

```
[api]
dist_git_token = YOUR_DIST_GIT_TOKEN_HERE
anitya_token = YOUR_ANITYA_TOKEN_HERE
```

To onboard a package:

```
$ fedora-sig-onboard onboard rust-escape_string
[rust-escape_string] updating ACL
[rust-escape_string] updating Bugzilla assignees
[rust-escape_string] adding to release monitoring
$
```

Multiple packages can also be specified, and will be processed in sequence. If no package is specified, `fedora-sig-onboard` will attempt to infer the package name from the current directory.

## License
`fedora-sig-onboard` is MIT licensed.
