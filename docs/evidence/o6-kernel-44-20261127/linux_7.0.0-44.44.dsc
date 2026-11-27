-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA512

Format: 1.0
Source: linux
Binary: linux-headers-7.0.0-44, linux-tools-7.0.0-44, linux-cloud-tools-7.0.0-44, linux-libc-dev, linux-tools-common, linux-cloud-tools-common, linux-tools-host, linux-source-7.0.0, linux-doc, linux-bpf-dev, bpftool, linux-perf, linux-image-unsigned-7.0.0-44-generic, linux-image-unsigned-7.0.0-44-generic-dbgsym, linux-image-7.0.0-44-generic, linux-image-7.0.0-44-generic-dbgsym, linux-modules-7.0.0-44-generic, linux-headers-7.0.0-44-generic, linux-lib-rust-7.0.0-44-generic, linux-tools-7.0.0-44-generic, linux-cloud-tools-7.0.0-44-generic, linux-buildinfo-7.0.0-44-generic, linux-image-unsigned-7.0.0-44-generic-64k, linux-image-unsigned-7.0.0-44-generic-64k-dbgsym, linux-modules-7.0.0-44-generic-64k, linux-headers-7.0.0-44-generic-64k, linux-lib-rust-7.0.0-44-generic-64k, linux-tools-7.0.0-44-generic-64k, linux-cloud-tools-7.0.0-44-generic-64k, linux-buildinfo-7.0.0-44-generic-64k
Architecture: all amd64 armhf arm64 ppc64el s390x i386 riscv64
Version: 7.0.0-44.44
Maintainer: Ubuntu Kernel Team <kernel-team@lists.ubuntu.com>
Standards-Version: 3.9.4.0
Vcs-Git: git://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/resolute
Build-Depends: gcc:native, gcc-aarch64-linux-gnu [arm64] <cross>, gcc-arm-linux-gnueabihf [armhf] <cross>, gcc-powerpc64le-linux-gnu [ppc64el] <cross>, gcc-riscv64-linux-gnu [riscv64] <cross>, gcc-s390x-linux-gnu [s390x] <cross>, gcc-x86-64-linux-gnu [amd64] <cross>, autoconf <!stage1>, automake <!stage1>, bc <!stage1>, bindgen:native [amd64 arm64 armhf ppc64el riscv64 s390x], bison <!stage1>, clang-21:native [amd64 arm64 armhf ppc64el riscv64 s390x], cpio, curl <!stage1>, debhelper-compat (= 10), default-jdk-headless:native <!stage1>, dkms <!stage1>, flex <!stage1>, gawk <!stage1>, java-common <!stage1>, kmod <!stage1>, libaudit-dev <!stage1>, libbpf-dev <!stage1>, libcap-dev <!stage1>, libdebuginfod-dev [amd64 arm64 armhf ppc64el s390x riscv64] <!stage1>, libdw-dev <!stage1>, libelf-dev <!stage1>, libiberty-dev <!stage1>, libllvm21 <!stage1>, liblzma-dev <!stage1>, libnewt-dev <!stage1>, libnl-3-dev, libnl-genl-3-dev, libnuma-dev [amd64 arm64 ppc64el s390x] <!stage1>, libpci-dev <!stage1>, libssl-dev <!stage1>, libstd-rust-dev [amd64 arm64 armhf ppc64el riscv64 s390x], libstdc++-dev, libtool <!stage1>, libtraceevent-dev [amd64 arm64 armhf ppc64el s390x riscv64] <!stage1>, libtracefs-dev [amd64 arm64 armhf ppc64el s390x riscv64] <!stage1>, libudev-dev <!stage1>, libunwind8-dev [amd64 arm64 armhf ppc64el] <!stage1>, llvm-21-tools:native <!stage1>, makedumpfile:native [amd64] <!stage1>, openssl <!stage1>, pahole (>= 1.29-2ubuntu2) [amd64 arm64 armhf ppc64el s390x riscv64] | dwarves (>= 1.21) [amd64 arm64 armhf ppc64el s390x riscv64] <!stage1>, pkg-config <!stage1>, python3:native <!stage1>, python3-dev:native <!stage1>, libpython3-dev <!stage1> <cross>, python3-setuptools, rsync [!i386] <!stage1>, rust-src:native [amd64 arm64 armhf ppc64el riscv64 s390x], rustc:native (>= 1.82) [amd64 arm64 armhf ppc64el riscv64 s390x], rustfmt:native [amd64 arm64 armhf ppc64el riscv64 s390x], uuid-dev <!stage1>, zstd <!stage1>, bpftool:native [amd64 arm64 armhf ppc64el riscv64 s390x] <!stage1 cross>
Build-Depends-Indep: asciidoc <!stage1>, bzip2 <!stage1>, python3-docutils <!stage1>, sharutils <!stage1>, xmlto <!stage1>
Package-List:
 bpftool deb devel optional arch=amd64,armhf,arm64,ppc64el,riscv64,s390x
 linux-bpf-dev deb devel optional arch=amd64,armhf,arm64,i386,ppc64el,riscv64,s390x
 linux-buildinfo-7.0.0-44-generic deb kernel optional arch=amd64,armhf,arm64,ppc64el,s390x profile=!stage1 profile:v1=!stage1
 linux-buildinfo-7.0.0-44-generic-64k deb kernel optional arch=arm64 profile=!stage1 profile:v1=!stage1
 linux-cloud-tools-7.0.0-44 deb devel optional arch=amd64,armhf profile=!stage1 profile:v1=!stage1
 linux-cloud-tools-7.0.0-44-generic deb devel optional arch=amd64,armhf,arm64,ppc64el,s390x profile=!stage1 profile:v1=!stage1
 linux-cloud-tools-7.0.0-44-generic-64k deb devel optional arch=arm64 profile=!stage1 profile:v1=!stage1
 linux-cloud-tools-common deb kernel optional arch=all profile=!stage1 profile:v1=!stage1
 linux-doc deb doc optional arch=all profile=!stage1 profile:v1=!stage1
 linux-headers-7.0.0-44 deb devel optional arch=all profile=!stage1 profile:v1=!stage1
 linux-headers-7.0.0-44-generic deb devel optional arch=amd64,armhf,arm64,ppc64el,s390x profile=!stage1 profile:v1=!stage1
 linux-headers-7.0.0-44-generic-64k deb devel optional arch=arm64 profile=!stage1 profile:v1=!stage1
 linux-image-7.0.0-44-generic deb kernel optional arch=armhf,ppc64el profile=!stage1 profile:v1=!stage1
 linux-image-7.0.0-44-generic-dbgsym deb devel optional arch=armhf,ppc64el profile=!stage1 profile:v1=!stage1
 linux-image-unsigned-7.0.0-44-generic deb kernel optional arch=amd64,arm64,s390x profile=!stage1 profile:v1=!stage1
 linux-image-unsigned-7.0.0-44-generic-64k deb kernel optional arch=arm64 profile=!stage1 profile:v1=!stage1
 linux-image-unsigned-7.0.0-44-generic-64k-dbgsym deb devel optional arch=arm64 profile=!stage1 profile:v1=!stage1
 linux-image-unsigned-7.0.0-44-generic-dbgsym deb devel optional arch=amd64,arm64,s390x profile=!stage1 profile:v1=!stage1
 linux-lib-rust-7.0.0-44-generic deb devel optional arch=amd64 profile=!stage1 profile:v1=!stage1
 linux-lib-rust-7.0.0-44-generic-64k deb devel optional arch=amd64 profile=!stage1 profile:v1=!stage1
 linux-libc-dev deb devel optional arch=amd64,armhf,arm64,i386,ppc64el,riscv64,s390x
 linux-modules-7.0.0-44-generic deb kernel optional arch=amd64,armhf,arm64,ppc64el,s390x profile=!stage1 profile:v1=!stage1
 linux-modules-7.0.0-44-generic-64k deb kernel optional arch=arm64 profile=!stage1 profile:v1=!stage1
 linux-perf deb devel optional arch=amd64,armhf,arm64,ppc64el,riscv64,s390x
 linux-source-7.0.0 deb devel optional arch=all profile=!stage1 profile:v1=!stage1
 linux-tools-7.0.0-44 deb devel optional arch=amd64,armhf,arm64,ppc64el,s390x profile=!stage1 profile:v1=!stage1
 linux-tools-7.0.0-44-generic deb devel optional arch=amd64,armhf,arm64,ppc64el,s390x profile=!stage1 profile:v1=!stage1
 linux-tools-7.0.0-44-generic-64k deb devel optional arch=arm64 profile=!stage1 profile:v1=!stage1
 linux-tools-common deb kernel optional arch=all profile=!stage1 profile:v1=!stage1
 linux-tools-host deb kernel optional arch=all profile=!stage1 profile:v1=!stage1
Checksums-Sha1:
 84ccdabedcb5eb28af56989b6070cfa864a325a9 254937830 linux_7.0.0.orig.tar.gz
 56198fa6c57ba2e55b91664d954d1a8e72a5bcb3 6286278 linux_7.0.0-44.44.diff.gz
Checksums-Sha256:
 c6343795c8c7e4feff55f5b309365c8e0eaf49cd6abcb412e32315313f149536 254937830 linux_7.0.0.orig.tar.gz
 fbfcc40c9367170fb6a83e5b0528cb94a992352785ac87fc7d8cdcd9426837c3 6286278 linux_7.0.0-44.44.diff.gz
Files:
 415e5d4ee110d9415c2901751e6f9c9d 254937830 linux_7.0.0.orig.tar.gz
 4ad8e85e0e23b226baa0cf82925d8b60 6286278 linux_7.0.0-44.44.diff.gz
Ubuntu-Compatible-Signing: ubuntu/4 pro/3 livepatch:2025 kmod:2025

-----BEGIN PGP SIGNATURE-----

iQIzBAEBCgAdFiEEOdMBrFJziXWR5e+rkdhqW2QaBCYFAmrtLiEACgkQkdhqW2Qa
BCYqGw//fG7F35dvwMGQkkTN7AatS5xJk8oQuVqvYR4veHunWZVsFODXlgYfmeFk
KYsWbkK7DnttZkbKkOuN1Kbj97VNIBz+WWTImEm/bu5kQxslnk06a2CsnQegmEzW
8bRmLg9ya3LpB2lf5S2wgzLSxLQmkVPsoV9jQNb6ayRTOzx72w90Tu8DhAz+6T7b
Y6Ddni0jWS+uv4x5jvMfmDZ/AFOXqo71HdamhUM0oh6G1z+Q/rkTUf91aEXzp6X4
ZpfmbEjrOY5D7bZeuzvHGJP+lsrvH7VDblcHpag/n5kGTVitqoa6Ykg/s7+bmnEJ
/JVAGG2v5v6XEPH+MI89Lp5itywpqghvXrVPFv+97lJVKzPOULzj7zq5LTIbO51K
hF7eE0YMK8zDN/RdlDN8QInvum3EBG3C0c/6iJEexLxbDTXx/IloOukhUOdVtfBy
Qd3bT3Qonnf36bAufww8mb7GaGrDTjfFAsxrrBV4OHUpsNDQ1y3WS9yvu5vlM9Gd
camFtvadJz88AIo/1uW7Xtj5IVnpklMAfTczLySCIdxYW6r0LNLNzHYhUZt++llb
GA+5lIJdSrOuqfsu8CYS9dLdStCl+BHmEe2yuNBaaVn0xh4Ney435E3IfRUioosd
uaI7plV1AeFbti9bbl8DuZZ7myzWrFAOSOuNpXFl4wsunJ6T5k8=
=jeEp
-----END PGP SIGNATURE-----
