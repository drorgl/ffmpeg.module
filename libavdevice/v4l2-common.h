/*
 * This file is part of FFmpeg.
 *
 * FFmpeg is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * FFmpeg is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with FFmpeg; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
 */

#ifndef AVDEVICE_V4L2_COMMON_H
#define AVDEVICE_V4L2_COMMON_H

#undef __STRICT_ANSI__ //workaround due to broken kernel headers
#include "config.h"
#include "libavformat/internal.h"
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/mman.h>
#include <sys/time.h>
#if HAVE_SYS_VIDEOIO_H
#include <sys/videoio.h>
#else
#if HAVE_ASM_TYPES_H
#include <asm/types.h>
#endif
#include <linux/videodev2.h>
#endif
#include "libavutil/atomic.h"
#include "libavutil/avassert.h"
#include "libavutil/imgutils.h"
#include "libavutil/log.h"
#include "libavutil/opt.h"
#include "avdevice.h"
#include "timefilter.h"
#include "libavutil/parseutils.h"
#include "libavutil/pixdesc.h"
#include "libavutil/avtime.h"
#include "libavutil/avstring.h"

struct fmt_map {
    enum AVPixelFormat ff_fmt;
    enum AVCodecID codec_id;
    uint32_t v4l2_fmt;
};

extern av_export const struct fmt_map avpriv_fmt_conversion_table[];

uint32_t avpriv_fmt_ff2v4l(enum AVPixelFormat pix_fmt, enum AVCodecID codec_id);
enum AVPixelFormat avpriv_fmt_v4l2ff(uint32_t v4l2_fmt, enum AVCodecID codec_id);
enum AVCodecID avpriv_fmt_v4l2codec(uint32_t v4l2_fmt);

#if !HAVE_STRUCT_V4L2_FRMIVALENUM_DISCRETE
#define VIDIOC_ENUM_FRAMESIZES	_IOWR('V', 74, struct v4l2_frmsizeenum)
enum v4l2_frmsizetypes {
	V4L2_FRMSIZE_TYPE_DISCRETE	= 1,
	V4L2_FRMSIZE_TYPE_CONTINUOUS	= 2,
	V4L2_FRMSIZE_TYPE_STEPWISE	= 3,
};

struct v4l2_frmsize_discrete {
	__u32			width;		/* Frame width [pixel] */
	__u32			height;		/* Frame height [pixel] */
};

struct v4l2_frmsize_stepwise {
	__u32			min_width;	/* Minimum frame width [pixel] */
	__u32			max_width;	/* Maximum frame width [pixel] */
	__u32			step_width;	/* Frame width step size [pixel] */
	__u32			min_height;	/* Minimum frame height [pixel] */
	__u32			max_height;	/* Maximum frame height [pixel] */
	__u32			step_height;	/* Frame height step size [pixel] */
};

struct v4l2_frmsizeenum {
	__u32			index;		/* Frame size number */
	__u32			pixel_format;	/* Pixel format */
	__u32			type;		/* Frame size type the device supports. */

	union {					/* Frame size */
		struct v4l2_frmsize_discrete	discrete;
		struct v4l2_frmsize_stepwise	stepwise;
	};

	__u32   reserved[2];			/* Reserved space for future use */
};

#endif

#endif /* AVDEVICE_V4L2_COMMON_H */
