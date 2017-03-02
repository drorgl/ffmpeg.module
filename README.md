# FFMPEG GYP Module

### **Experimental **

Expose FFMPEG libraries through gyp, splitting huge modules like libavcodec to multiple projects so cygwin will be able to build them without crashing on path is too long

* config folder for each os/architecture
* windows specific fix to snprintf in compat/msvcrt/snprinf.c (might not be needed)
* android specific fix in libavdevice/v4l2.c and v4l2-common.h (might not be needed)

requires vsyasm assembler for windows build or yasm for linux

#### known issues:
* HAVE_STRERROR_R is not set in configs, need to check why
* android v4l2 is broken, the fixes are in the repo but need to adjust to newer ffmpeg code
* I don't understand the following lines from libavutil/internal.h, but they interfere with compilation in vs2013, remark them.

```
#if defined(_MSC_VER)
#pragma comment(linker, "/include:"EXTERN_PREFIX"avpriv_strtod")
#pragma comment(linker, "/include:"EXTERN_PREFIX"avpriv_snprintf")
#endif
```

#### compiling with gyp
```
compiling for win32:
gyp ffmpeg.gyp -Dtarget_arch=ia32 --depth=. -f msvs -G msvs_version=2013 --generator-output=./build.vs2013/

compiling for win64:
gyp ffmpeg.gyp -Dtarget_arch=x64 --depth=. -f msvs -G msvs_version=2013 --generator-output=./build.vs2013/

compiling for linux32:
gyp ffmpeg.gyp -Dtarget_arch=ia32 -DOS=linux --depth=. -f make --generator-output=./build.make/

compiling for linux64:
gyp ffmpeg.gyp -Dtarget_arch=x64 -DOS=linux --depth=. -f make --generator-output=./build.make/

compiling for android/arm:
gyp ffmpeg.gyp -Dtarget_arch=arm -DOS=android --depth=. -f make --generator-output=./build.make/

compiling for linux/android with ninja:
replace -f make with -f ninja

compiling 32 bit linux on 64 bit linux:
sudo apt-get install lib32stdc++6-4.8-dbg
```

Requires GCC 4.9 (NDK 10) for android/arm build for performance purposes.

#### Dependencies

##### zlib
>
>https://github.com/drorgl/zlib.module
>
>origin: https://github.com/madler/zlib

##### x264
>
>https://github.com/drorgl/x264.module
>
>origin: http://git.videolan.org/git/x264.git

##### lame
>
>https://github.com/drorgl/lame.module
>
>origin: http://lame.sourceforge.net/

##### alsa-lib
>
>https://github.com/drorgl/alsa-lib.module
>
>origin: git://git.alsa-project.org/alsa-lib.git


##### libvpx 
>
>https://github.com/drorgl/libvpx.module
>
>origin: https://github.com/openpeer/libvpx.git



### FFmpeg License
FFmpeg is licensed under the GNU Lesser General Public License (LGPL) version 2.1 or later. However, FFmpeg incorporates several optional parts and optimizations that are covered by the GNU General Public License (GPL) version 2 or later. If those parts get used the GPL applies to all of FFmpeg.

Read the license texts to learn how this affects programs built on top of FFmpeg or reusing FFmpeg. You may also wish to have a look at the GPL FAQ.

Note that FFmpeg is not available under any other licensing terms, especially not proprietary/commercial ones, not even in exchange for payment.


#### FFMPEG Legal links:
https://www.ffmpeg.org/legal.html

https://www.ffmpeg.org/doxygen/2.6/md_LICENSE.html

I've made an attempt to split GPL and nonfree modules configuration to their own files. 

### ** THERE MAY BE LICENSING MISTAKES IN THE GYP FILE! IF YOU PLAN ON USING THIS IN A COMMERCIAL SOFTWARE DO YOUR OWN VALIDATION AND CONSULT YOUR LEGAL DEPT.! **

to enable gpl components you need to modify variable use_gpl_components in ffmpeg.gyp and modify each platform gpl_config.h and nonfree_config.h

