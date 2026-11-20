-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA512

Format: 1.0
Source: linux
Binary: linux-headers-7.0.0-43, linux-tools-7.0.0-43, linux-cloud-tools-7.0.0-43, linux-libc-dev, linux-tools-common, linux-cloud-tools-common, linux-tools-host, linux-source-7.0.0, linux-doc, linux-bpf-dev, bpftool, linux-perf, linux-image-unsigned-7.0.0-43-generic, linux-image-unsigned-7.0.0-43-generic-dbgsym, linux-image-7.0.0-43-generic, linux-image-7.0.0-43-generic-dbgsym, linux-modules-7.0.0-43-generic, linux-headers-7.0.0-43-generic, linux-lib-rust-7.0.0-43-generic, linux-tools-7.0.0-43-generic, linux-cloud-tools-7.0.0-43-generic, linux-buildinfo-7.0.0-43-generic, linux-image-unsigned-7.0.0-43-generic-64k, linux-image-unsigned-7.0.0-43-generic-64k-dbgsym, linux-modules-7.0.0-43-generic-64k, linux-headers-7.0.0-43-generic-64k, linux-lib-rust-7.0.0-43-generic-64k, linux-tools-7.0.0-43-generic-64k, linux-cloud-tools-7.0.0-43-generic-64k, linux-buildinfo-7.0.0-43-generic-64k
Architecture: all amd64 armhf arm64 ppc64el s390x i386 riscv64
Version: 7.0.0-43.43
Maintainer: Ubuntu Kernel Team <kernel-team@lists.ubuntu.com>
Standards-Version: 3.9.4.0
Vcs-Git: git://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/resolute
Build-Depends: gcc:native, gcc-aarch64-linux-gnu [arm64] <cross>, gcc-arm-linux-gnueabihf [armhf] <cross>, gcc-powerpc64le-linux-gnu [ppc64el] <cross>, gcc-riscv64-linux-gnu [riscv64] <cross>, gcc-s390x-linux-gnu [s390x] <cross>, gcc-x86-64-linux-gnu [amd64] <cross>, autoconf <!stage1>, automake <!stage1>, bc <!stage1>, bindgen:native [amd64 arm64 armhf ppc64el riscv64 s390x], bison <!stage1>, clang-21:native [amd64 arm64 armhf ppc64el riscv64 s390x], cpio, curl <!stage1>, debhelper-compat (= 10), default-jdk-headless:native <!stage1>, dkms <!stage1>, flex <!stage1>, gawk <!stage1>, java-common <!stage1>, kmod <!stage1>, libaudit-dev <!stage1>, libbpf-dev <!stage1>, libcap-dev <!stage1>, libdebuginfod-dev [amd64 arm64 armhf ppc64el s390x riscv64] <!stage1>, libdw-dev <!stage1>, libelf-dev <!stage1>, libiberty-dev <!stage1>, libllvm21 <!stage1>, liblzma-dev <!stage1>, libnewt-dev <!stage1>, libnl-3-dev, libnl-genl-3-dev, libnuma-dev [amd64 arm64 ppc64el s390x] <!stage1>, libpci-dev <!stage1>, libssl-dev <!stage1>, libstd-rust-dev [amd64 arm64 armhf ppc64el riscv64 s390x], libstdc++-dev, libtool <!stage1>, libtraceevent-dev [amd64 arm64 armhf ppc64el s390x riscv64] <!stage1>, libtracefs-dev [amd64 arm64 armhf ppc64el s390x riscv64] <!stage1>, libudev-dev <!stage1>, libunwind8-dev [amd64 arm64 armhf ppc64el] <!stage1>, llvm-21-tools:native <!stage1>, makedumpfile:native [amd64] <!stage1>, openssl <!stage1>, pahole (>= 1.29-2ubuntu2) [amd64 arm64 armhf ppc64el s390x riscv64] | dwarves (>= 1.21) [amd64 arm64 armhf ppc64el s390x riscv64] <!stage1>, pkg-config <!stage1>, python3:native <!stage1>, python3-dev:native <!stage1>, libpython3-dev <!stage1> <cross>, python3-setuptools, rsync [!i386] <!stage1>, rust-src:native [amd64 arm64 armhf ppc64el riscv64 s390x], rustc:native (>= 1.82) [amd64 arm64 armhf ppc64el riscv64 s390x], rustfmt:native [amd64 arm64 armhf ppc64el riscv64 s390x], uuid-dev <!stage1>, zstd <!stage1>, bpftool:native [amd64 arm64 armhf ppc64el riscv64 s390x] <!stage1 cross>
Build-Depends-Indep: asciidoc <!stage1>, bzip2 <!stage1>, python3-docutils <!stage1>, sharutils <!stage1>, xmlto <!stage1>
Package-List:
 bpftool deb devel optional arch=amd64,armhf,arm64,ppc64el,riscv64,s390x
 linux-bpf-dev deb devel optional arch=amd64,armhf,arm64,i386,ppc64el,riscv64,s390x
 linux-buildinfo-7.0.0-43-generic deb kernel optional arch=amd64,armhf,arm64,ppc64el,s390x profile=!stage1 profile:v1=!stage1
 linux-buildinfo-7.0.0-43-generic-64k deb kernel optional arch=arm64 profile=!stage1 profile:v1=!stage1
 linux-cloud-tools-7.0.0-43 deb devel optional arch=amd64,armhf profile=!stage1 profile:v1=!stage1
 linux-cloud-tools-7.0.0-43-generic deb devel optional arch=amd64,armhf,arm64,ppc64el,s390x profile=!stage1 profile:v1=!stage1
 linux-cloud-tools-7.0.0-43-generic-64k deb devel optional arch=arm64 profile=!stage1 profile:v1=!stage1
 linux-cloud-tools-common deb kernel optional arch=all profile=!stage1 profile:v1=!stage1
 linux-doc deb doc optional arch=all profile=!stage1 profile:v1=!stage1
 linux-headers-7.0.0-43 deb devel optional arch=all profile=!stage1 profile:v1=!stage1
 linux-headers-7.0.0-43-generic deb devel optional arch=amd64,armhf,arm64,ppc64el,s390x profile=!stage1 profile:v1=!stage1
 linux-headers-7.0.0-43-generic-64k deb devel optional arch=arm64 profile=!stage1 profile:v1=!stage1
 linux-image-7.0.0-43-generic deb kernel optional arch=armhf,ppc64el profile=!stage1 profile:v1=!stage1
 linux-image-7.0.0-43-generic-dbgsym deb devel optional arch=armhf,ppc64el profile=!stage1 profile:v1=!stage1
 linux-image-unsigned-7.0.0-43-generic deb kernel optional arch=amd64,arm64,s390x profile=!stage1 profile:v1=!stage1
 linux-image-unsigned-7.0.0-43-generic-64k deb kernel optional arch=arm64 profile=!stage1 profile:v1=!stage1
 linux-image-unsigned-7.0.0-43-generic-64k-dbgsym deb devel optional arch=arm64 profile=!stage1 profile:v1=!stage1
 linux-image-unsigned-7.0.0-43-generic-dbgsym deb devel optional arch=amd64,arm64,s390x profile=!stage1 profile:v1=!stage1
 linux-lib-rust-7.0.0-43-generic deb devel optional arch=amd64 profile=!stage1 profile:v1=!stage1
 linux-lib-rust-7.0.0-43-generic-64k deb devel optional arch=amd64 profile=!stage1 profile:v1=!stage1
 linux-libc-dev deb devel optional arch=amd64,armhf,arm64,i386,ppc64el,riscv64,s390x
 linux-modules-7.0.0-43-generic deb kernel optional arch=amd64,armhf,arm64,ppc64el,s390x profile=!stage1 profile:v1=!stage1
 linux-modules-7.0.0-43-generic-64k deb kernel optional arch=arm64 profile=!stage1 profile:v1=!stage1
 linux-perf deb devel optional arch=amd64,armhf,arm64,ppc64el,riscv64,s390x
 linux-source-7.0.0 deb devel optional arch=all profile=!stage1 profile:v1=!stage1
 linux-tools-7.0.0-43 deb devel optional arch=amd64,armhf,arm64,ppc64el,s390x profile=!stage1 profile:v1=!stage1
 linux-tools-7.0.0-43-generic deb devel optional arch=amd64,armhf,arm64,ppc64el,s390x profile=!stage1 profile:v1=!stage1
 linux-tools-7.0.0-43-generic-64k deb devel optional arch=arm64 profile=!stage1 profile:v1=!stage1
 linux-tools-common deb kernel optional arch=all profile=!stage1 profile:v1=!stage1
 linux-tools-host deb kernel optional arch=all profile=!stage1 profile:v1=!stage1
Checksums-Sha1:
 84ccdabedcb5eb28af56989b6070cfa864a325a9 254937830 linux_7.0.0.orig.tar.gz
 00f2229587bb0176115e87b1fbd4b039afe71841 6172264 linux_7.0.0-43.43.diff.gz
Checksums-Sha256:
 c6343795c8c7e4feff55f5b309365c8e0eaf49cd6abcb412e32315313f149536 254937830 linux_7.0.0.orig.tar.gz
 8ab260d7af287e5fcb6117e4866ef9d6256ce72b6f3f920203d09b1703c57b83 6172264 linux_7.0.0-43.43.diff.gz
Files:
 415e5d4ee110d9415c2901751e6f9c9d 254937830 linux_7.0.0.orig.tar.gz
 8aff21b1c9dc2de0cd37bb63abae339b 6172264 linux_7.0.0-43.43.diff.gz
Ubuntu-Compatible-Signing: ubuntu/4 pro/3 livepatch:2025 kmod:2025

-----BEGIN PGP SIGNATURE-----

iQIzBAEBCgAdFiEE2118yvOZTjOV2k0+6Gdd7svuzqMFAmrbUCYACgkQ6Gdd7svu
zqOpzw//dFmJzm4GFCtTazdYELAcDPlLwJPtvcqqTuw9dEmrKi2/QIe4s6NTyJKG
/UPbRo1wdROuSEDpETEGo8CJbpF5pmhWNIMg7wbWRWKQ9fZh4Z3bWZimm37b5vnF
1aA8dXyh3/YuTjdhDRkph2q8WaBp9Y88OAU7aFF0Ae/qvrwymUcDhrY/bUU9BrHT
30oijnCADQHjdJYrdtFADmCTV5N4wEmBoBU+LzTPJ+XHby25EfJRPF4pBz5eKx4v
vlJuj/fcYiDphJPww/KA6NeYCx7zuaqY2XDXFXGdTdjx9QC+BmdHZ3CfPt6usUMd
03rqVML0dPpMkt13wsX467NdG1aoL/19Wd4Wt883BY1idG+pntAkuv24Z3TwRV57
GXwCZLo57R78gtpNmXw7Bp8p0Th2Om0/nUVakXeNv9wPyd0tscF1QZmSyYZK3crS
l2TTyQQJ1eiuGfXNQTOCOp05BmjTIPnUPTyjtRb8yvzDFiK+9uPNBXbVlhXlsrEi
47ramK6L89B+93UBK0eNy4nLzHrMDqowfnCwLWljhWs6F8SLPBmoIi4tRP8V/1yd
xxkllBl4I+srIQvhUX+p1iT5o8gKgXgoMotmt9HuPnp2khjmkjd4ZqLeWLjUPWYf
k/1wMGC3ErZiP5L+LkqM1tCeStPFbQbT+2TT58uFGivcLLtwkPI=
=wkaC
-----END PGP SIGNATURE-----
