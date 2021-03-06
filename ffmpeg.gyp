{
	'variables':{
		'library' : 'static_library',
		'primary_libraries' : 'shared_library',
		#'primary_libraries' : 'static_library',
		'use_system_yasm%' : "<!(node -e \"try{var x = require('child_process').spawnSync('yasm',[]);if (x.error){console.log(0);}else{console.log(1);}}catch(e){console.log(0)}\")",
		'use_gpl_components' : '1',
		 'yasm_output_path': '<(INTERMEDIATE_DIR)',

	},
	'target_defaults': {
		'defines':[	
			'HAVE_AV_CONFIG_H',
			#'avpriv_strtod=strtod'
		],
		'include_dirs':[
			'config/<(OS)/<(target_arch)',
			'./'
		],
		
		'direct_dependent_settings': {
			'include_dirs': [
				'./',
				'ffmpeg_src',
			],
		 },
		'msvs_settings': {
			# This magical incantation is necessary because VC++ will compile
			# object files to same directory... even if they have the same name!
			'VCCLCompilerTool': {
				'ForcedIncludeFiles' : ['stdint.h'],
			  'ObjectFile': '$(IntDir)/%(RelativeDir)/',
			  'AdditionalOptions': ['/GL-'], #['/wd4244' ,'/wd4018','/wd4133' ,'/wd4090'] #GL- was added because the forced optimization coming from node-gyp is disturbing the weird coding style from ffmpeg.
			  'WholeProgramOptimization' : 'false',
			},
			
		},
		
		'configurations': {
			'Debug' : {
				'conditions':[
					['1==1',{
						'msvs_settings': {
							# This magical incantation is necessary because VC++ will compile
							# object files to same directory... even if they have the same name!
							'VCCLCompilerTool': {
							  'WholeProgramOptimization' : 'false',
							  'BasicRuntimeChecks' : '0',
							  'Optimization' : '1', # /O1
							  'AdditionalOptions': ['/GL-'], #['/wd4244' ,'/wd4018','/wd4133' ,'/wd4090'] #GL- was added because the forced optimization coming from node-gyp is disturbing the weird coding style from ffmpeg.
							},
							'VCLinkerTool': {
							  'LinkTimeCodeGeneration': '0',
							  'GenerateDebugInformation': 'true',
							  
								'conditions':[
									['target_arch=="x64"', {
										'TargetMachine' : 17 # /MACHINE:X64
									}],
									
								],
							  
							},
							
							'VCLibrarianTool': {
								'AdditionalOptions!': ['/LTCG'],
							 },
							
						}
				}],
				['target_arch=="x64"', {
					'msvs_configuration_platform': 'x64',
				}],
				]
			},
			'Release' : {
				'conditions':[
					['1==1',{
						'msvs_settings': {
							# This magical incantation is necessary because VC++ will compile
							# object files to same directory... even if they have the same name!
							'VCCLCompilerTool': {
							  'WholeProgramOptimization' : 'false',
							  'AdditionalOptions': ['/GL-'], #['/wd4244' ,'/wd4018','/wd4133' ,'/wd4090'] #GL- was added because the forced optimization coming from node-gyp is disturbing the weird coding style from ffmpeg.
							},
							'VCLinkerTool': {
							  'LinkTimeCodeGeneration': '0',
							  
								'conditions':[
									['target_arch=="x64"', {
										'TargetMachine' : 17 # /MACHINE:X64
									}],
								],
							  
							},
							
							'VCLibrarianTool': {
								'AdditionalOptions!': ['/LTCG'],
							 },
							
						}
					}],
					['target_arch=="x64"', {
						'msvs_configuration_platform': 'x64',
					}],
				]
			},
		},
		
		'conditions': [
			['OS=="linux" and target_arch=="ia32"',{
				'cflags':[
					'-m32',
				],
				'ldflags':[
					'-m32',
					'-L/usr/lib32',
					'-L/usr/lib32/debug',
				],
			}],
			['OS=="linux" and target_arch=="x64"',{
				'cflags':[
					'-m64'
				],
				'ldflags':[
					'-m64',
				],
			}],
			[ 'OS in "win linux" and target_arch=="ia32"', {
				'defines':[
					'ARCH_X86_64=0',
					'ARCH_X86_32=1',
				],
			}],
			[ 'OS in "win linux" and target_arch=="x64"', {
				'defines':[
					'ARCH_X86_64=1',
					'ARCH_X86_32=0',
				],
			}],
			[ 'OS in "linux android" and target_arch=="arm"',{
				'defines':[
					'_DEFAULT_SOURCE'
				],
			}],
			['OS == "win"',{
				'defines':[
					'inline=__inline',
					'__asm__=__asm',
				],
				'include_dirs':[
					#'config/windows',
				],

			}],
			['OS != "win" and primary_libraries == "shared_library"',{
				'cflags':[
					'-fPIC',
				],	
				'defines':[
					'PIC',
				],
			}],
		  ['OS != "win"', {
			'defines': [
			  '_LARGEFILE_SOURCE',
			  '_FILE_OFFSET_BITS=64',
			],
			'include_dirs':[
					#'config/android',
				],
			'cflags':[
				'-std=gnu99',
				'-Wno-traditional',
				'-Wno-sign-compare',
				'-Wno-switch',
				'-Wno-missing-field-initializers',
				'-Wno-parentheses',
				'-Wno-pointer-sign',
				'-Wno-unused-function',
				'-Wno-old-style-declaration'
				#'-include stdint.h',
			],
			'conditions': [
			  ['OS=="solaris"', {
				'cflags': [ '-pthreads' ],
			  }],
			  ['OS not in "solaris android"', {
				'cflags': [ '-pthread' ],
			  }],
			],
		}],
		['OS in "android linux" and target_arch=="arm"',{
			#'include_dirs':[
			#	'config/android'
			#],
			'defines':[
				'ANDROID'
			],
			'cflags':[
				'-marm',
				'-march=armv7-a',
				'-mfpu=neon',
				'-mfloat-abi=hard',
				'-funsafe-math-optimizations',
			],
		}],
	  
		['use_gpl_components == 1',{
			'defines':[
				'ENABLE_GPL=1',
			],
		}],
		  
		  
		],
	  },
	'targets':
	[
		{
			'target_name':'avcodec',
			'type':'<(primary_libraries)',
			'sources' : [
				'definitions/avcodec.def',
				'ffmpeg_src/libavcodec/allcodecs.c',
				'ffmpeg_src/libavcodec/options.c',
				'ffmpeg_src/libavcodec/utils.c',
				'ffmpeg_src/libavcodec/codec_desc.c',
				'ffmpeg_src/libavcodec/bitstream_filter.c',
				'ffmpeg_src/libavcodec/avpicture.c',
				'ffmpeg_src/libavcodec/avpacket.c',
				'ffmpeg_src/libavcodec/parser.c',
				
				'ffmpeg_src/libavcodec/aacadtsdec.c',
				'ffmpeg_src/libavcodec/exif.c',
				'ffmpeg_src/libavcodec/bitstream.c',
				'ffmpeg_src/libavcodec/imgconvert.c',
				'ffmpeg_src/libavcodec/avdct.c',
				'ffmpeg_src/libavcodec/ac3_parser.c',
				'ffmpeg_src/libavcodec/ac3tab.c',
				'ffmpeg_src/libavcodec/avfft.c',
				'ffmpeg_src/libavcodec/mpegaudiodecheader.c',
				'ffmpeg_src/libavcodec/mpegaudiodata.c',
				'ffmpeg_src/libavcodec/dca.c',
				'ffmpeg_src/libavcodec/dnxhddata.c',
				'ffmpeg_src/libavcodec/vorbis_parser.c',
				'ffmpeg_src/libavcodec/mjpeg.c',
				'ffmpeg_src/libavcodec/raw.c',
				'ffmpeg_src/libavcodec/xiph.c',
				'ffmpeg_src/libavcodec/dv_profile.c',
				'ffmpeg_src/libavcodec/elbg.c',
				'ffmpeg_src/libavcodec/tak.c',
				'ffmpeg_src/libavcodec/mpeg4audio.c',
				'ffmpeg_src/libavcodec/h264.c',
				'ffmpeg_src/libavcodec/dirac.c',
			],
			'direct_dependent_settings': {
				'include_dirs': [
					'ffmpeg_src/libavcodec',
				],
			 },
			'dependencies':[
				'avcodec_p1',
				'avcodec_p2',
				'avcodec_p3',
				'avcodec_p4',
				'avutil',
				'swresample',
				'<!@(nnbu-dependency --dependency vpx)',
				#'../libvpx.module/libvpx.gyp:libvpx',
			],
			'include_dirs':[
				'<!@(nnbu-dependency --headers vpx)',
			],
			'link_settings':{
					'libraries':[
						'<!@(nnbu-dependency --lib-fix --libs vpx)',
					],
			 },
			'conditions':[
				['use_gpl_components == 1',{
					'dependencies':[
						'<!@(nnbu-dependency --dependency x264)',
					],
					'include_dirs':[
						'<!@(nnbu-dependency --headers x264)',
					],
					'link_settings':{
							'libraries':[
								'<!@(nnbu-dependency --lib-fix --libs x264)',
							],
					},
					
					'sources':[
						'ffmpeg_src/libavcodec/libx264.c',
					],
				}]
			],
		},
		
		{
			'target_name': 'avcodec_p1',
			'type':'<(library)',
			'dependencies':[
				'avutil',
			],
			'defines':[],
			'include_dirs':[
				'ffmpeg_src',
				'ffmpeg_src/libavcodec',
			],
			'direct_dependent_settings': {
				'include_dirs': [
					'ffmpeg_src/libavcodec',
				],
			 },
			 
			 

			
			 
			'sources':[
				
				
				'ffmpeg_src/libavcodec/012v.c',
				'ffmpeg_src/libavcodec/4xm.c',
				'ffmpeg_src/libavcodec/8bps.c',
				'ffmpeg_src/libavcodec/8svx.c',
				'ffmpeg_src/libavcodec/a64multienc.c',
				
				'ffmpeg_src/libavcodec/aaccoder.c',
				'ffmpeg_src/libavcodec/aacdec.c',
				'ffmpeg_src/libavcodec/aacenc.c',
				'ffmpeg_src/libavcodec/aacps.c',
				#'ffmpeg_src/libavcodec/aacpsdata.c',
				'ffmpeg_src/libavcodec/aacpsdsp.c',
				'ffmpeg_src/libavcodec/aacpsy.c',
				'ffmpeg_src/libavcodec/aacsbr.c',
				'ffmpeg_src/libavcodec/aactab.c',
				'ffmpeg_src/libavcodec/aac_ac3_parser.c',
				'ffmpeg_src/libavcodec/aac_adtstoasc_bsf.c',
				'ffmpeg_src/libavcodec/aac_parser.c',
				'ffmpeg_src/libavcodec/aandcttab.c',
				'ffmpeg_src/libavcodec/aasc.c',
				
				'ffmpeg_src/libavcodec/acelp_filters.c',
				'ffmpeg_src/libavcodec/acelp_pitch_delay.c',
				'ffmpeg_src/libavcodec/acelp_vectors.c',
				'ffmpeg_src/libavcodec/adpcm.c',
				'ffmpeg_src/libavcodec/adpcmenc.c',
				'ffmpeg_src/libavcodec/adpcm_data.c',
				'ffmpeg_src/libavcodec/adx.c',
				'ffmpeg_src/libavcodec/adxdec.c',
				'ffmpeg_src/libavcodec/adxenc.c',
				'ffmpeg_src/libavcodec/adx_parser.c',
				'ffmpeg_src/libavcodec/aic.c',
				'ffmpeg_src/libavcodec/alac.c',
				'ffmpeg_src/libavcodec/alacenc.c',
				'ffmpeg_src/libavcodec/alac_data.c',
				
				'ffmpeg_src/libavcodec/alsdec.c',
				'ffmpeg_src/libavcodec/amrnbdec.c',
				'ffmpeg_src/libavcodec/amrwbdec.c',
				'ffmpeg_src/libavcodec/anm.c',
				'ffmpeg_src/libavcodec/ansi.c',
				'ffmpeg_src/libavcodec/apedec.c',
				'ffmpeg_src/libavcodec/ass.c',
				'ffmpeg_src/libavcodec/assdec.c',
				'ffmpeg_src/libavcodec/assenc.c',
				'ffmpeg_src/libavcodec/ass_split.c',
				'ffmpeg_src/libavcodec/asv.c',
				'ffmpeg_src/libavcodec/asvdec.c',
				'ffmpeg_src/libavcodec/asvenc.c',
				'ffmpeg_src/libavcodec/atrac.c',
				'ffmpeg_src/libavcodec/atrac1.c',
				'ffmpeg_src/libavcodec/atrac3.c',
				'ffmpeg_src/libavcodec/atrac3plus.c',
				'ffmpeg_src/libavcodec/atrac3plusdec.c',
				'ffmpeg_src/libavcodec/atrac3plusdsp.c',
				'ffmpeg_src/libavcodec/audioconvert.c',
				'ffmpeg_src/libavcodec/audio_frame_queue.c',
				'ffmpeg_src/libavcodec/aura.c',
				
				
				
				'ffmpeg_src/libavcodec/avrndec.c',
				'ffmpeg_src/libavcodec/avs.c',
				'ffmpeg_src/libavcodec/avuidec.c',
				'ffmpeg_src/libavcodec/avuienc.c',
				'ffmpeg_src/libavcodec/bethsoftvideo.c',
				'ffmpeg_src/libavcodec/bfi.c',
				'ffmpeg_src/libavcodec/bgmc.c',
				'ffmpeg_src/libavcodec/bink.c',
				'ffmpeg_src/libavcodec/binkaudio.c',
				'ffmpeg_src/libavcodec/binkdsp.c',
				'ffmpeg_src/libavcodec/bintext.c',
				
				
				'ffmpeg_src/libavcodec/bmp.c',
				'ffmpeg_src/libavcodec/bmpenc.c',
				'ffmpeg_src/libavcodec/bmp_parser.c',
				#'ffmpeg_src/libavcodec/bmv.c',
				'ffmpeg_src/libavcodec/brenderpix.c',
				'ffmpeg_src/libavcodec/c93.c',
				'ffmpeg_src/libavcodec/cabac.c',
				'ffmpeg_src/libavcodec/cavs.c',
				'ffmpeg_src/libavcodec/cavsdata.c',
				'ffmpeg_src/libavcodec/cavsdec.c',
				'ffmpeg_src/libavcodec/cavsdsp.c',
				'ffmpeg_src/libavcodec/cavs_parser.c',
				'ffmpeg_src/libavcodec/cdgraphics.c',
				'ffmpeg_src/libavcodec/cdxl.c',
				'ffmpeg_src/libavcodec/celp_filters.c',
				'ffmpeg_src/libavcodec/celp_math.c',
				'ffmpeg_src/libavcodec/cga_data.c',
				'ffmpeg_src/libavcodec/chomp_bsf.c',
				'ffmpeg_src/libavcodec/cinepak.c',
				'ffmpeg_src/libavcodec/cinepakenc.c',
				#'ffmpeg_src/libavcodec/cljr.c',
				'ffmpeg_src/libavcodec/cllc.c',
				'ffmpeg_src/libavcodec/cngdec.c',
				'ffmpeg_src/libavcodec/cngenc.c',
				
				'ffmpeg_src/libavcodec/cook.c',
				'ffmpeg_src/libavcodec/cook_parser.c',
				'ffmpeg_src/libavcodec/cpia.c',
				'ffmpeg_src/libavcodec/cscd.c',
				'ffmpeg_src/libavcodec/cyuv.c',
				
				'ffmpeg_src/libavcodec/dcadec.c',
				'ffmpeg_src/libavcodec/dcadsp.c',
				'ffmpeg_src/libavcodec/dcaenc.c',
				'ffmpeg_src/libavcodec/dca_parser.c',
				'ffmpeg_src/libavcodec/dct.c',
				'ffmpeg_src/libavcodec/dct32_fixed.c',
				'ffmpeg_src/libavcodec/dct32_float.c',
				'ffmpeg_src/libavcodec/dctref.c',
				'ffmpeg_src/libavcodec/dfa.c',
				
				'ffmpeg_src/libavcodec/diracdec.c',
				'ffmpeg_src/libavcodec/diracdsp.c',
				'ffmpeg_src/libavcodec/dirac_arith.c',
				'ffmpeg_src/libavcodec/dirac_dwt.c',
				'ffmpeg_src/libavcodec/dirac_parser.c',
				
				'ffmpeg_src/libavcodec/dnxhddec.c',
				'ffmpeg_src/libavcodec/dnxhdenc.c',
				'ffmpeg_src/libavcodec/dnxhd_parser.c',
				'ffmpeg_src/libavcodec/dpcm.c',
				'ffmpeg_src/libavcodec/dpx.c',
				'ffmpeg_src/libavcodec/dpxenc.c',
				'ffmpeg_src/libavcodec/dpx_parser.c',
				#'ffmpeg_src/libavcodec/dsicinav.c',
				#'ffmpeg_src/libavcodec/dsputil.c',
				'ffmpeg_src/libavcodec/dump_extradata_bsf.c',
				'ffmpeg_src/libavcodec/dv.c',
				'ffmpeg_src/libavcodec/dvbsub.c',
				'ffmpeg_src/libavcodec/dvbsubdec.c',
				'ffmpeg_src/libavcodec/dvbsub_parser.c',
				'ffmpeg_src/libavcodec/dvdata.c',
				'ffmpeg_src/libavcodec/dvdec.c',
				'ffmpeg_src/libavcodec/dvdsubdec.c',
				'ffmpeg_src/libavcodec/dvdsubenc.c',
				'ffmpeg_src/libavcodec/dvdsub_parser.c',
				'ffmpeg_src/libavcodec/dvd_nav_parser.c',
				'ffmpeg_src/libavcodec/dvenc.c',
				
				'ffmpeg_src/libavcodec/dxa.c',
				'ffmpeg_src/libavcodec/dxtory.c',
				#'ffmpeg_src/libavcodec/eac3dec.c',
				'ffmpeg_src/libavcodec/eac3enc.c',
				'ffmpeg_src/libavcodec/eac3_data.c',
				'ffmpeg_src/libavcodec/eacmv.c',
				'ffmpeg_src/libavcodec/eaidct.c',
				'ffmpeg_src/libavcodec/eamad.c',
				'ffmpeg_src/libavcodec/eatgq.c',
				'ffmpeg_src/libavcodec/eatgv.c',
				'ffmpeg_src/libavcodec/eatqi.c',
				
				'ffmpeg_src/libavcodec/error_resilience.c',
				'ffmpeg_src/libavcodec/escape124.c',
				'ffmpeg_src/libavcodec/escape130.c',
				'ffmpeg_src/libavcodec/evrcdec.c',
				
				'ffmpeg_src/libavcodec/exr.c',
				'ffmpeg_src/libavcodec/faandct.c',
				'ffmpeg_src/libavcodec/faanidct.c',
				'ffmpeg_src/libavcodec/faxcompr.c',
				
				'ffmpeg_src/libavcodec/ffv1.c',
				'ffmpeg_src/libavcodec/ffv1dec.c',
				'ffmpeg_src/libavcodec/ffv1enc.c',
				'ffmpeg_src/libavcodec/ffwavesynth.c',
				'ffmpeg_src/libavcodec/fic.c',
				'ffmpeg_src/libavcodec/file_open.c',
				'ffmpeg_src/libavcodec/flac.c',
				'ffmpeg_src/libavcodec/flacdata.c',
				'ffmpeg_src/libavcodec/flacdec.c',	
				'ffmpeg_src/libavcodec/flacdsp.c',
				'ffmpeg_src/libavcodec/flacenc.c',
				'ffmpeg_src/libavcodec/flac_parser.c',
				'ffmpeg_src/libavcodec/flashsv.c',
				'ffmpeg_src/libavcodec/flashsv2enc.c',
				'ffmpeg_src/libavcodec/flashsvenc.c',
				'ffmpeg_src/libavcodec/flicvideo.c',
				'ffmpeg_src/libavcodec/flvdec.c',
				'ffmpeg_src/libavcodec/flvenc.c',
				'ffmpeg_src/libavcodec/fmtconvert.c',
				'ffmpeg_src/libavcodec/frame_thread_encoder.c',
				
			],
			'conditions':[
				['OS=="linux"',{
					'cflags':[
						'-fvisibility=hidden',
					],
				}],
				['target_arch in "ia32 x64"',{
					'includes':[
						'yasm_compile.gypi',
					 ],
					 'variables':{
						'yasm_paths':[
							'-I','ffmpeg_src',
							'-I','config/<(OS)/<(target_arch)',
						],
						'yasm_flags':[
							'-Pconfig.asm',
							'-DPIC=1',
						 ],
					 },
				}],
				['OS == "win"',{
					'dependencies':[
						'<!@(nnbu-dependency --dependency zlib)',
					],
					'include_dirs':[
						'<!@(nnbu-dependency --headers zlib)',
					],
					'link_settings':{
							'libraries':[
								'<!@(nnbu-dependency --lib-fix --libs zlib)',
							],
					},
					
				}],
			]
		},
		
			{
			'target_name': 'avcodec_p2',
			'type':'<(library)',
			'dependencies':[		
				'<!@(nnbu-dependency --dependency lame)',
				#'../lame.module/lame.gyp:libmp3lame',
				'avutil',
			],
			'defines':[],
			'include_dirs':[
				'ffmpeg_src',
				'ffmpeg_src/libavcodec',
				'<!@(nnbu-dependency --headers lame)',
			],
			'link_settings':{
					'libraries':[
						'<!@(nnbu-dependency --lib-fix --libs lame)',
					],
			},
			'direct_dependent_settings': {
				'include_dirs': [
					'ffmpeg_src/libavcodec',
				],
			 },
			 

			
			 
			'sources':[
				
				'ffmpeg_src/libavcodec/fraps.c',
				'ffmpeg_src/libavcodec/frwu.c',
				'ffmpeg_src/libavcodec/g2meet.c',
				'ffmpeg_src/libavcodec/g722.c',
				'ffmpeg_src/libavcodec/g722dec.c',
				'ffmpeg_src/libavcodec/g722enc.c',
				'ffmpeg_src/libavcodec/g723_1.c',
				'ffmpeg_src/libavcodec/g726.c',
				'ffmpeg_src/libavcodec/g729dec.c',
				'ffmpeg_src/libavcodec/g729postfilter.c',
				'ffmpeg_src/libavcodec/gif.c',
				'ffmpeg_src/libavcodec/gifdec.c',
				'ffmpeg_src/libavcodec/golomb.c',
				'ffmpeg_src/libavcodec/gsmdec.c',
				'ffmpeg_src/libavcodec/gsmdec_data.c',
				'ffmpeg_src/libavcodec/gsm_parser.c',
				'ffmpeg_src/libavcodec/h261.c',
				'ffmpeg_src/libavcodec/h261data.c',
				'ffmpeg_src/libavcodec/h261dec.c',
				'ffmpeg_src/libavcodec/h261enc.c',
				'ffmpeg_src/libavcodec/h261_parser.c',
				'ffmpeg_src/libavcodec/h263.c',
				'ffmpeg_src/libavcodec/h263dec.c',
				'ffmpeg_src/libavcodec/h263dsp.c',
				'ffmpeg_src/libavcodec/h263_parser.c',
				
				'ffmpeg_src/libavcodec/h264chroma.c',
				'ffmpeg_src/libavcodec/h264dsp.c',
				'ffmpeg_src/libavcodec/h264idct.c',
				'ffmpeg_src/libavcodec/h264pred.c',
				'ffmpeg_src/libavcodec/h264qpel.c',
				'ffmpeg_src/libavcodec/h264_cabac.c',
				'ffmpeg_src/libavcodec/h264_cavlc.c',
				'ffmpeg_src/libavcodec/h264_direct.c',
				'ffmpeg_src/libavcodec/h264_loopfilter.c',
				'ffmpeg_src/libavcodec/h264_mp4toannexb_bsf.c',
				'ffmpeg_src/libavcodec/h264_mb.c',
				'ffmpeg_src/libavcodec/h264_parser.c',
				'ffmpeg_src/libavcodec/h264_picture.c',
				'ffmpeg_src/libavcodec/h264_ps.c',
				'ffmpeg_src/libavcodec/h264_refs.c',
				'ffmpeg_src/libavcodec/h264_sei.c',
				'ffmpeg_src/libavcodec/h264_slice.c',
				'ffmpeg_src/libavcodec/hevc.c',
				'ffmpeg_src/libavcodec/hevcdsp.c',
				'ffmpeg_src/libavcodec/hevcpred.c',
				'ffmpeg_src/libavcodec/hevc_cabac.c',
				'ffmpeg_src/libavcodec/hevc_filter.c',
				'ffmpeg_src/libavcodec/hevc_mvs.c',
				'ffmpeg_src/libavcodec/hevc_parser.c',
				'ffmpeg_src/libavcodec/hevc_ps.c',
				'ffmpeg_src/libavcodec/hevc_refs.c',
				'ffmpeg_src/libavcodec/hevc_sei.c',
				'ffmpeg_src/libavcodec/hnm4video.c',
				'ffmpeg_src/libavcodec/hpeldsp.c',
				'ffmpeg_src/libavcodec/huffman.c',
				'ffmpeg_src/libavcodec/huffyuv.c',
				'ffmpeg_src/libavcodec/huffyuvdec.c',
				'ffmpeg_src/libavcodec/huffyuvenc.c',
				'ffmpeg_src/libavcodec/huffyuvencdsp.c',
				
				'ffmpeg_src/libavcodec/idcinvideo.c',
				'ffmpeg_src/libavcodec/iff.c',
				'ffmpeg_src/libavcodec/iirfilter.c',
				'ffmpeg_src/libavcodec/imc.c',
				
				'ffmpeg_src/libavcodec/imx_dump_header_bsf.c',
				'ffmpeg_src/libavcodec/indeo2.c',
				'ffmpeg_src/libavcodec/indeo3.c',
				'ffmpeg_src/libavcodec/indeo4.c',
				'ffmpeg_src/libavcodec/indeo5.c',
				'ffmpeg_src/libavcodec/intelh263dec.c',
				'ffmpeg_src/libavcodec/interplayvideo.c',
				'ffmpeg_src/libavcodec/intrax8.c',
				'ffmpeg_src/libavcodec/intrax8dsp.c',
				'ffmpeg_src/libavcodec/ituh263dec.c',
				'ffmpeg_src/libavcodec/ituh263enc.c',
				'ffmpeg_src/libavcodec/ivi_common.c',
				
				'ffmpeg_src/libavcodec/ivi_dsp.c',
				'ffmpeg_src/libavcodec/j2kenc.c',
				'ffmpeg_src/libavcodec/jacosubdec.c',
				'ffmpeg_src/libavcodec/jfdctfst.c',
			
				'ffmpeg_src/libavcodec/jfdctint.c',
				'ffmpeg_src/libavcodec/jpeg2000.c',
				'ffmpeg_src/libavcodec/jpeg2000dec.c',
				'ffmpeg_src/libavcodec/jpeg2000dwt.c',
				'ffmpeg_src/libavcodec/jpeg2000dsp.c',
				
				
				'ffmpeg_src/libavcodec/jpegls.c',
				'ffmpeg_src/libavcodec/jpeglsdec.c',
				'ffmpeg_src/libavcodec/jpeglsenc.c',
				'ffmpeg_src/libavcodec/jrevdct.c',
				'ffmpeg_src/libavcodec/jvdec.c',
				
				'ffmpeg_src/libavcodec/kbdwin.c',
				'ffmpeg_src/libavcodec/kgv1dec.c',
				'ffmpeg_src/libavcodec/kmvc.c',
				'ffmpeg_src/libavcodec/lagarith.c',
				'ffmpeg_src/libavcodec/lagarithrac.c',
				'ffmpeg_src/libavcodec/latm_parser.c',
				'ffmpeg_src/libavcodec/lcldec.c',
				'ffmpeg_src/libavcodec/lclenc.c',
				'ffmpeg_src/libavcodec/ljpegenc.c',
				'ffmpeg_src/libavcodec/loco.c',
				'ffmpeg_src/libavcodec/log2_tab.c',
				'ffmpeg_src/libavcodec/lossless_videodsp.c',
				'ffmpeg_src/libavcodec/lpc.c',
				'ffmpeg_src/libavcodec/lsp.c',
				'ffmpeg_src/libavcodec/lzw.c',
				'ffmpeg_src/libavcodec/lzwenc.c',
				'ffmpeg_src/libavcodec/mace.c',
				'ffmpeg_src/libavcodec/mathtables.c',
				'ffmpeg_src/libavcodec/mdct_fixed.c',
				'ffmpeg_src/libavcodec/mdct_fixed_32.c',
				'ffmpeg_src/libavcodec/mdct_float.c',
				'ffmpeg_src/libavcodec/mdec.c',
				'ffmpeg_src/libavcodec/metasound.c',
				'ffmpeg_src/libavcodec/metasound_data.c',
				'ffmpeg_src/libavcodec/microdvddec.c',
				'ffmpeg_src/libavcodec/mimic.c',
				
				'ffmpeg_src/libavcodec/mjpeg2jpeg_bsf.c',
				'ffmpeg_src/libavcodec/mjpega_dump_header_bsf.c',
				'ffmpeg_src/libavcodec/mjpegbdec.c',
				'ffmpeg_src/libavcodec/mjpegdec.c',
				'ffmpeg_src/libavcodec/mjpegenc.c',
				'ffmpeg_src/libavcodec/mjpeg_parser.c',
				'ffmpeg_src/libavcodec/mlp.c',
				'ffmpeg_src/libavcodec/mlpdec.c',
				'ffmpeg_src/libavcodec/mlpdsp.c',
				'ffmpeg_src/libavcodec/mlp_parser.c',
				'ffmpeg_src/libavcodec/mmvideo.c',
				'ffmpeg_src/libavcodec/motionpixels.c',
				'ffmpeg_src/libavcodec/motion_est.c',
				'ffmpeg_src/libavcodec/movsub_bsf.c',
				'ffmpeg_src/libavcodec/movtextdec.c',
				'ffmpeg_src/libavcodec/movtextenc.c',
					
				'ffmpeg_src/libavcodec/mp3_header_decompress_bsf.c',
				'ffmpeg_src/libavcodec/libmp3lame.c',
				'ffmpeg_src/libavcodec/mpc.c',
				'ffmpeg_src/libavcodec/mpc7.c',
				'ffmpeg_src/libavcodec/mpc8.c',
				'ffmpeg_src/libavcodec/mpeg12.c',
				'ffmpeg_src/libavcodec/mpeg12data.c',
				'ffmpeg_src/libavcodec/mpeg12dec.c',
				'ffmpeg_src/libavcodec/mpeg12enc.c',
				
				'ffmpeg_src/libavcodec/mpeg4video.c',
				'ffmpeg_src/libavcodec/mpeg4videodec.c',
				'ffmpeg_src/libavcodec/mpeg4videoenc.c',
				'ffmpeg_src/libavcodec/mpeg4video_parser.c',
				'ffmpeg_src/libavcodec/mpegaudio.c',
				
				
				'ffmpeg_src/libavcodec/mpegaudiodec_fixed.c',
				'ffmpeg_src/libavcodec/mpegaudiodec_float.c',
				'ffmpeg_src/libavcodec/mpegaudiodsp.c',
				'ffmpeg_src/libavcodec/mpegaudiodsp_data.c',
				'ffmpeg_src/libavcodec/mpegaudiodsp_fixed.c',
				'ffmpeg_src/libavcodec/mpegaudiodsp_float.c',
				'ffmpeg_src/libavcodec/mpegaudioenc_fixed.c',
				'ffmpeg_src/libavcodec/mpegaudioenc_float.c',
				'ffmpeg_src/libavcodec/mpegaudio_parser.c',
				'ffmpeg_src/libavcodec/mpegutils.c',
				'ffmpeg_src/libavcodec/mpegvideo.c',
				'ffmpeg_src/libavcodec/mpegvideo_enc.c',
				'ffmpeg_src/libavcodec/mpegvideo_motion.c',
				'ffmpeg_src/libavcodec/mpegvideo_parser.c',
				
				'ffmpeg_src/libavcodec/mpl2dec.c',
				'ffmpeg_src/libavcodec/mqc.c',
				'ffmpeg_src/libavcodec/mqcdec.c',
				'ffmpeg_src/libavcodec/mqcenc.c',
				'ffmpeg_src/libavcodec/msgsmdec.c',
				'ffmpeg_src/libavcodec/msmpeg4.c',
				'ffmpeg_src/libavcodec/msmpeg4data.c',
				'ffmpeg_src/libavcodec/msmpeg4dec.c',
				'ffmpeg_src/libavcodec/msmpeg4enc.c',
				'ffmpeg_src/libavcodec/msrle.c',
				'ffmpeg_src/libavcodec/msrledec.c',
				'ffmpeg_src/libavcodec/mss1.c',
				'ffmpeg_src/libavcodec/mss12.c',
				'ffmpeg_src/libavcodec/mss2.c',
				'ffmpeg_src/libavcodec/mss2dsp.c',
				'ffmpeg_src/libavcodec/mss3.c',
				'ffmpeg_src/libavcodec/mss34dsp.c',
				'ffmpeg_src/libavcodec/mss4.c',
				
			],
			'conditions':[
				['OS=="linux"',{
					'cflags':[
						'-fvisibility=hidden',
					],
				}],
				['target_arch in "ia32 x64"',{
					'includes':[
						'yasm_compile.gypi',
					 ],
					 'variables':{
						'yasm_flags':[
							'-I','ffmpeg_src',
							'-I','config/<(OS)/<(target_arch)',
							'-Pconfig.asm',
							'-DPIC=1',
						 ],
					 },
				}],

				['OS == "win"',{
					
					
					'dependencies':[
						'<!@(nnbu-dependency --dependency zlib)',
					],
					'include_dirs':[
						'<!@(nnbu-dependency --headers zlib)',
					],
					'link_settings':{
							'libraries':[
								'<!@(nnbu-dependency --lib-fix --libs zlib)',
							],
					},
				}],
			]
		},
	
			{
			'target_name': 'avcodec_p3',
			'type':'<(library)',
			'dependencies':[
				#'../lame.module/lame.gyp:libmp3lame',
				'<!@(nnbu-dependency --dependency lame)',
				'avutil',
			],
			'defines':[],
			'include_dirs':[
				'ffmpeg_src',
				'ffmpeg_src/libavcodec',
				'<!@(nnbu-dependency --headers lame)',
			],
			'direct_dependent_settings': {
				'include_dirs': [
					'ffmpeg_src/libavcodec',
				],
			 },
			 'link_settings':{
					'libraries':[
						'<!@(nnbu-dependency --lib-fix --libs lame)',
					],
			},
			 
			 

			
			 
			'sources':[
				
			
				
				
				'ffmpeg_src/libavcodec/msvideo1.c',
				'ffmpeg_src/libavcodec/msvideo1enc.c',
				'ffmpeg_src/libavcodec/mvcdec.c',
				'ffmpeg_src/libavcodec/mxpegdec.c',
				'ffmpeg_src/libavcodec/nellymoser.c',
				'ffmpeg_src/libavcodec/nellymoserdec.c',
				'ffmpeg_src/libavcodec/nellymoserenc.c',
				'ffmpeg_src/libavcodec/noise_bsf.c',
				'ffmpeg_src/libavcodec/nuv.c',
				
				#'ffmpeg_src/libavcodec/paf.c',
				'ffmpeg_src/libavcodec/pamenc.c',
				
				'ffmpeg_src/libavcodec/pcm-bluray.c',
				'ffmpeg_src/libavcodec/pcm-dvd.c',
				'ffmpeg_src/libavcodec/pcm.c',
				'ffmpeg_src/libavcodec/pcx.c',
				'ffmpeg_src/libavcodec/pcxenc.c',
				'ffmpeg_src/libavcodec/pgssubdec.c',
				'ffmpeg_src/libavcodec/pictordec.c',
				'ffmpeg_src/libavcodec/png.c',
				'ffmpeg_src/libavcodec/pngdec.c',
				'ffmpeg_src/libavcodec/pngdsp.c',
				'ffmpeg_src/libavcodec/pngenc.c',
				'ffmpeg_src/libavcodec/png_parser.c',
				'ffmpeg_src/libavcodec/pnm.c',
				'ffmpeg_src/libavcodec/pnmdec.c',
				'ffmpeg_src/libavcodec/pnmenc.c',
				'ffmpeg_src/libavcodec/pnm_parser.c',
				'ffmpeg_src/libavcodec/proresdata.c',
				'ffmpeg_src/libavcodec/proresdec2.c',
				'ffmpeg_src/libavcodec/proresdec_lgpl.c',
				'ffmpeg_src/libavcodec/proresdsp.c',
				'ffmpeg_src/libavcodec/proresenc_anatoliy.c',
				'ffmpeg_src/libavcodec/proresenc_kostya.c',
				'ffmpeg_src/libavcodec/psymodel.c',
				'ffmpeg_src/libavcodec/pthread.c',
				'ffmpeg_src/libavcodec/pthread_frame.c',
				'ffmpeg_src/libavcodec/pthread_slice.c',
				'ffmpeg_src/libavcodec/ptx.c',
				'ffmpeg_src/libavcodec/qcelpdec.c',
				'ffmpeg_src/libavcodec/qdm2.c',
				'ffmpeg_src/libavcodec/qdrw.c',
				'ffmpeg_src/libavcodec/qpeg.c',
				'ffmpeg_src/libavcodec/qtrle.c',
				'ffmpeg_src/libavcodec/qtrleenc.c',
				'ffmpeg_src/libavcodec/r210dec.c',
				'ffmpeg_src/libavcodec/r210enc.c',
				'ffmpeg_src/libavcodec/ra144.c',
				'ffmpeg_src/libavcodec/ra144dec.c',
				'ffmpeg_src/libavcodec/ra144enc.c',
				'ffmpeg_src/libavcodec/ra288.c',
				'ffmpeg_src/libavcodec/ralf.c',
				'ffmpeg_src/libavcodec/rangecoder.c',
				'ffmpeg_src/libavcodec/ratecontrol.c',
				
				'ffmpeg_src/libavcodec/rawdec.c',
				'ffmpeg_src/libavcodec/rawenc.c',
				'ffmpeg_src/libavcodec/rdft.c',
				'ffmpeg_src/libavcodec/realtextdec.c',
				'ffmpeg_src/libavcodec/remove_extradata_bsf.c',
				'ffmpeg_src/libavcodec/resample.c',
				'ffmpeg_src/libavcodec/resample2.c',
				'ffmpeg_src/libavcodec/rl2.c',
				'ffmpeg_src/libavcodec/rle.c',
				'ffmpeg_src/libavcodec/roqaudioenc.c',
				'ffmpeg_src/libavcodec/roqvideo.c',
				'ffmpeg_src/libavcodec/roqvideodec.c',
				'ffmpeg_src/libavcodec/roqvideoenc.c',
				'ffmpeg_src/libavcodec/rpza.c',
				'ffmpeg_src/libavcodec/rtjpeg.c',
				'ffmpeg_src/libavcodec/rv10.c',
				'ffmpeg_src/libavcodec/rv10enc.c',
				'ffmpeg_src/libavcodec/rv20enc.c',
				'ffmpeg_src/libavcodec/rv30.c',
				'ffmpeg_src/libavcodec/rv30dsp.c',
				'ffmpeg_src/libavcodec/rv34.c',
				'ffmpeg_src/libavcodec/rv34dsp.c',
				'ffmpeg_src/libavcodec/rv34_parser.c',
				'ffmpeg_src/libavcodec/rv40.c',
				'ffmpeg_src/libavcodec/rv40dsp.c',
				'ffmpeg_src/libavcodec/s302m.c',
				'ffmpeg_src/libavcodec/s302menc.c',
				'ffmpeg_src/libavcodec/s3tc.c',
				'ffmpeg_src/libavcodec/samidec.c',
				'ffmpeg_src/libavcodec/sanm.c',
				'ffmpeg_src/libavcodec/sbrdsp.c',
				'ffmpeg_src/libavcodec/sgidec.c',
				'ffmpeg_src/libavcodec/sgienc.c',
				'ffmpeg_src/libavcodec/sgirledec.c',
				'ffmpeg_src/libavcodec/shorten.c',
				'ffmpeg_src/libavcodec/simple_idct.c',
				'ffmpeg_src/libavcodec/sinewin.c',
				'ffmpeg_src/libavcodec/sipr.c',
				'ffmpeg_src/libavcodec/sipr16k.c',
				'ffmpeg_src/libavcodec/smacker.c',
				'ffmpeg_src/libavcodec/smc.c',
				'ffmpeg_src/libavcodec/smvjpegdec.c',
				'ffmpeg_src/libavcodec/snow.c',
				'ffmpeg_src/libavcodec/snowdec.c',
				'ffmpeg_src/libavcodec/snowenc.c',
				'ffmpeg_src/libavcodec/snow_dwt.c',
				'ffmpeg_src/libavcodec/sonic.c',
				'ffmpeg_src/libavcodec/sp5xdec.c',
				'ffmpeg_src/libavcodec/srtdec.c',
				'ffmpeg_src/libavcodec/srtenc.c',
				'ffmpeg_src/libavcodec/startcode.c',
				'ffmpeg_src/libavcodec/subviewerdec.c',
				'ffmpeg_src/libavcodec/sunrast.c',
				'ffmpeg_src/libavcodec/sunrastenc.c',
				'ffmpeg_src/libavcodec/svq1.c',
				'ffmpeg_src/libavcodec/svq13.c',
				'ffmpeg_src/libavcodec/svq1dec.c',
				'ffmpeg_src/libavcodec/svq1enc.c',
				'ffmpeg_src/libavcodec/svq3.c',
				'ffmpeg_src/libavcodec/synth_filter.c',
				
				'ffmpeg_src/libavcodec/takdec.c',
				'ffmpeg_src/libavcodec/tak_parser.c',
				'ffmpeg_src/libavcodec/targa.c',
				'ffmpeg_src/libavcodec/targaenc.c',
				'ffmpeg_src/libavcodec/targa_y216dec.c',
				'ffmpeg_src/libavcodec/textdec.c',
				'ffmpeg_src/libavcodec/tiertexseqv.c',
				'ffmpeg_src/libavcodec/tiff.c',
				'ffmpeg_src/libavcodec/tiffenc.c',
				'ffmpeg_src/libavcodec/tiff_common.c',
				'ffmpeg_src/libavcodec/tiff_data.c',
				'ffmpeg_src/libavcodec/tmv.c',
				'ffmpeg_src/libavcodec/tpeldsp.c',
				'ffmpeg_src/libavcodec/truemotion1.c',
				'ffmpeg_src/libavcodec/truemotion2.c',
				'ffmpeg_src/libavcodec/truespeech.c',
				'ffmpeg_src/libavcodec/tscc.c',
				'ffmpeg_src/libavcodec/tscc2.c',
				'ffmpeg_src/libavcodec/tta.c',
				'ffmpeg_src/libavcodec/ttadata.c',
				'ffmpeg_src/libavcodec/ttadsp.c',
				'ffmpeg_src/libavcodec/ttaenc.c',
				'ffmpeg_src/libavcodec/twinvq.c',
				'ffmpeg_src/libavcodec/twinvqdec.c',
				'ffmpeg_src/libavcodec/txd.c',
				'ffmpeg_src/libavcodec/ulti.c',
				
				'ffmpeg_src/libavcodec/utvideo.c',
				'ffmpeg_src/libavcodec/utvideodec.c',
				'ffmpeg_src/libavcodec/utvideoenc.c',
				'ffmpeg_src/libavcodec/v210dec.c',
				'ffmpeg_src/libavcodec/v210enc.c',
				'ffmpeg_src/libavcodec/v210x.c',
				'ffmpeg_src/libavcodec/v308dec.c',
				'ffmpeg_src/libavcodec/v308enc.c',
				'ffmpeg_src/libavcodec/v408dec.c',
				'ffmpeg_src/libavcodec/v408enc.c',
				'ffmpeg_src/libavcodec/v410dec.c',
				'ffmpeg_src/libavcodec/v410enc.c',
				'ffmpeg_src/libavcodec/vb.c',
				'ffmpeg_src/libavcodec/vble.c',
				'ffmpeg_src/libavcodec/vc1.c',
				'ffmpeg_src/libavcodec/vc1data.c',
				'ffmpeg_src/libavcodec/vc1dec.c',
				'ffmpeg_src/libavcodec/vc1dsp.c',
				'ffmpeg_src/libavcodec/vc1_parser.c',
				'ffmpeg_src/libavcodec/vcr1.c',
				'ffmpeg_src/libavcodec/videodsp.c',
				'ffmpeg_src/libavcodec/vima.c',
				#'ffmpeg_src/libavcodec/vmdav.c',
				'ffmpeg_src/libavcodec/vmnc.c',
				'ffmpeg_src/libavcodec/vorbis.c',
				'ffmpeg_src/libavcodec/vorbisdec.c',
				'ffmpeg_src/libavcodec/vorbisdsp.c',
				'ffmpeg_src/libavcodec/vorbisenc.c',
				'ffmpeg_src/libavcodec/vorbis_data.c',
				
				'ffmpeg_src/libavcodec/vp3.c',
				'ffmpeg_src/libavcodec/vp3dsp.c',
				'ffmpeg_src/libavcodec/vp3_parser.c',
				'ffmpeg_src/libavcodec/vp5.c',
				'ffmpeg_src/libavcodec/vp56.c',
				'ffmpeg_src/libavcodec/vp56data.c',
				'ffmpeg_src/libavcodec/vp56dsp.c',
				'ffmpeg_src/libavcodec/vp56rac.c',
				'ffmpeg_src/libavcodec/vp6.c',
				'ffmpeg_src/libavcodec/vp6dsp.c',
				'ffmpeg_src/libavcodec/vp8.c',
				'ffmpeg_src/libavcodec/vp8dsp.c',
				'ffmpeg_src/libavcodec/vp8_parser.c',
				'ffmpeg_src/libavcodec/vp9.c',
				'ffmpeg_src/libavcodec/vp9dsp.c',
				'ffmpeg_src/libavcodec/vp9_parser.c',
				'ffmpeg_src/libavcodec/vqavideo.c',
				'ffmpeg_src/libavcodec/wavpack.c',
				'ffmpeg_src/libavcodec/webp.c',
				'ffmpeg_src/libavcodec/webvttdec.c',
				
			],
			'conditions':[
				['OS=="linux"',{
					'cflags':[
						'-fvisibility=hidden',
					],
				}],
				['target_arch in "ia32 x64"',{
					'includes':[
						'yasm_compile.gypi',
					 ],
					 'variables':{
						'yasm_flags':[
							'-I','ffmpeg_src',
							'-I','config/<(OS)/<(target_arch)',
							'-Pconfig.asm',
							'-DPIC=1',
						 ],
					 },
				}],

				['OS == "win"',{
					 
					'dependencies':[
						'<!@(nnbu-dependency --dependency zlib)',
					],
					'include_dirs':[
						'<!@(nnbu-dependency --headers zlib)',
					],
					'link_settings':{
						'libraries':[
							'<!@(nnbu-dependency --lib-fix --libs zlib)',
						],
					},
				}],
			]
		},
		
		
		{
			'target_name': 'avcodec_p4',
			'type':'<(library)',
			'dependencies':[
				#'../lame.module/lame.gyp:libmp3lame',
				'<!@(nnbu-dependency --dependency lame)',
				'<!@(nnbu-dependency --dependency vpx)',
				#'../libvpx.module/libvpx.gyp:libvpx',
				'avutil',
			],
			'defines':[],
			'include_dirs':[
				'ffmpeg_src',
				'ffmpeg_src/libavcodec',
				'<!@(nnbu-dependency --headers lame)',
				'<!@(nnbu-dependency --headers vpx)',
			],
			'direct_dependent_settings': {
				'include_dirs': [
					'ffmpeg_src/libavcodec',
				],
			 },
			 
			'export_dependent_settings':[
				#'../libvpx.module/libvpx.gyp:libvpx',
				'<!@(nnbu-dependency --dependency vpx)',
			 ],

			
			 
			'sources':[
				'ffmpeg_src/libavcodec/fft_fixed.c',
				'ffmpeg_src/libavcodec/fft_fixed_32.c',
				'ffmpeg_src/libavcodec/fft_float.c',
				'ffmpeg_src/libavcodec/fft_init_table.c',
				'ffmpeg_src/libavcodec/ac3.c',
				'ffmpeg_src/libavcodec/ac3dec_data.c',
				'ffmpeg_src/libavcodec/ac3dec_float.c',
				'ffmpeg_src/libavcodec/ac3dsp.c',
				'ffmpeg_src/libavcodec/ac3enc.c',
				'ffmpeg_src/libavcodec/ac3enc_fixed.c',
				'ffmpeg_src/libavcodec/ac3enc_float.c',
				
				
				
				'ffmpeg_src/libavcodec/imdct15.c',
				'ffmpeg_src/libavcodec/wma.c',
				'ffmpeg_src/libavcodec/wma_freqs.c',
				'ffmpeg_src/libavcodec/wmadec.c',
				'ffmpeg_src/libavcodec/wmaenc.c',
				'ffmpeg_src/libavcodec/wmalosslessdec.c',
				'ffmpeg_src/libavcodec/wmaprodec.c',
				'ffmpeg_src/libavcodec/wmavoice.c',
				'ffmpeg_src/libavcodec/wma_common.c',
				'ffmpeg_src/libavcodec/wmv2.c',
				'ffmpeg_src/libavcodec/wmv2dec.c',
				'ffmpeg_src/libavcodec/wmv2dsp.c',
				'ffmpeg_src/libavcodec/wmv2enc.c',
				'ffmpeg_src/libavcodec/wnv1.c',
				'ffmpeg_src/libavcodec/ws-snd1.c',
				'ffmpeg_src/libavcodec/xan.c',
				'ffmpeg_src/libavcodec/xbmdec.c',
				'ffmpeg_src/libavcodec/xbmenc.c',
				'ffmpeg_src/libavcodec/xface.c',
				'ffmpeg_src/libavcodec/xfacedec.c',
				'ffmpeg_src/libavcodec/xfaceenc.c',
				
				'ffmpeg_src/libavcodec/xl.c',
				'ffmpeg_src/libavcodec/xsubdec.c',
				'ffmpeg_src/libavcodec/xsubenc.c',
				'ffmpeg_src/libavcodec/xwddec.c',
				'ffmpeg_src/libavcodec/xwdenc.c',
				'ffmpeg_src/libavcodec/xxan.c',
				'ffmpeg_src/libavcodec/y41pdec.c',
				'ffmpeg_src/libavcodec/y41penc.c',
				'ffmpeg_src/libavcodec/yop.c',
				'ffmpeg_src/libavcodec/yuv4dec.c',
				'ffmpeg_src/libavcodec/yuv4enc.c',
				'ffmpeg_src/libavcodec/zerocodec.c',
				'ffmpeg_src/libavcodec/zmbv.c',
				'ffmpeg_src/libavcodec/zmbvenc.c',
				'ffmpeg_src/libavcodec/qpeldsp.c',
				'ffmpeg_src/libavcodec/vc1_block.c',
				'ffmpeg_src/libavcodec/mjpegenc_common.c',
				'ffmpeg_src/libavcodec/me_cmp.c',
				'ffmpeg_src/libavcodec/vc1_pred.c',
				'ffmpeg_src/libavcodec/vc1_loopfilter.c',
				'ffmpeg_src/libavcodec/g722dsp.c',
				'ffmpeg_src/libavcodec/dcadata.c',
				'ffmpeg_src/libavcodec/audiodsp.c',
				'ffmpeg_src/libavcodec/dss_sp.c',
				'ffmpeg_src/libavcodec/webvttenc.c',
				'ffmpeg_src/libavcodec/vc1_mc.c',
				'ffmpeg_src/libavcodec/mpeg_er.c',
				'ffmpeg_src/libavcodec/huffyuvdsp.c',
				'ffmpeg_src/libavcodec/mpegvideodsp.c',
				'ffmpeg_src/libavcodec/xvididct.c',
				'ffmpeg_src/libavcodec/idctdsp.c',
				'ffmpeg_src/libavcodec/dca_exss.c',
				'ffmpeg_src/libavcodec/lossless_audiodsp.c',
				'ffmpeg_src/libavcodec/bswapdsp.c',
				'ffmpeg_src/libavcodec/mpegvideoencdsp.c',
				'ffmpeg_src/libavcodec/blockdsp.c',
				'ffmpeg_src/libavcodec/pixblockdsp.c',
				'ffmpeg_src/libavcodec/fdctdsp.c',
				'ffmpeg_src/libavcodec/opus_parser.c',
				'ffmpeg_src/libavcodec/opus.c',
				#'ffmpeg_src/libavcodec/libopenh264enc.c',
				'ffmpeg_src/libavcodec/ccaption_dec.c',
				'ffmpeg_src/libavcodec/vmdaudio.c',
				'ffmpeg_src/libavcodec/pafaudio.c',
				'ffmpeg_src/libavcodec/opusdec.c',
				'ffmpeg_src/libavcodec/dsicinaudio.c',
				'ffmpeg_src/libavcodec/bmvaudio.c',
				'ffmpeg_src/libavcodec/bmvvideo.c',
				'ffmpeg_src/libavcodec/vmdvideo.c',
				'ffmpeg_src/libavcodec/pafvideo.c',
				#'ffmpeg_src/libavcodec/nvenc.c',
				'ffmpeg_src/libavcodec/hqx.c',
				'ffmpeg_src/libavcodec/hqxvlc.c',
				'ffmpeg_src/libavcodec/opus_silk.c',
				'ffmpeg_src/libavcodec/opus_celt.c',
				'ffmpeg_src/libavcodec/cljrenc.c',
				'ffmpeg_src/libavcodec/cljrdec.c',
				#'ffmpeg_src/libavcodec/qsv_h264.c',
				'ffmpeg_src/libavcodec/dsicinvideo.c',
				#'ffmpeg_src/libavcodec/dxva2_hevc.c',
				#'ffmpeg_src/libavcodec/vda_h264.c',
				'ffmpeg_src/libavcodec/libvpxdec.c',
				'ffmpeg_src/libavcodec/libvpxenc.c',
				'ffmpeg_src/libavcodec/libvpx.c',
				
				
			],
			'conditions':[
				['target_arch == "arm"',{
					
					'sources': [
						'ffmpeg_src/libavcodec/arm/aac.h',
						'ffmpeg_src/libavcodec/arm/aacpsdsp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/aacpsdsp_neon.S',
						'ffmpeg_src/libavcodec/arm/ac3dsp_arm.S',
						'ffmpeg_src/libavcodec/arm/ac3dsp_armv6.S',
						'ffmpeg_src/libavcodec/arm/ac3dsp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/ac3dsp_neon.S',
						'ffmpeg_src/libavcodec/arm/asm-offsets.h',
						'ffmpeg_src/libavcodec/arm/audiodsp_arm.h',
						'ffmpeg_src/libavcodec/arm/audiodsp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/audiodsp_init_neon.c',
						'ffmpeg_src/libavcodec/arm/audiodsp_neon.S',
						'ffmpeg_src/libavcodec/arm/blockdsp_arm.h',
						'ffmpeg_src/libavcodec/arm/blockdsp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/blockdsp_init_neon.c',
						'ffmpeg_src/libavcodec/arm/blockdsp_neon.S',
						'ffmpeg_src/libavcodec/arm/cabac.h',
						'ffmpeg_src/libavcodec/arm/dca.h',
						'ffmpeg_src/libavcodec/arm/dcadsp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/dcadsp_neon.S',
						'ffmpeg_src/libavcodec/arm/dcadsp_vfp.S',
						#'ffmpeg_src/libavcodec/arm/dct-test.c',
						'ffmpeg_src/libavcodec/arm/fft_fixed_init_arm.c',
						'ffmpeg_src/libavcodec/arm/fft_fixed_neon.S',
						'ffmpeg_src/libavcodec/arm/fft_init_arm.c',
						'ffmpeg_src/libavcodec/arm/fft_neon.S',
						'ffmpeg_src/libavcodec/arm/fft_vfp.S',
						'ffmpeg_src/libavcodec/arm/flacdsp_arm.S',
						'ffmpeg_src/libavcodec/arm/flacdsp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/fmtconvert_init_arm.c',
						'ffmpeg_src/libavcodec/arm/fmtconvert_neon.S',
						'ffmpeg_src/libavcodec/arm/fmtconvert_vfp.S',
						'ffmpeg_src/libavcodec/arm/g722dsp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/g722dsp_neon.S',
						'ffmpeg_src/libavcodec/arm/h264chroma_init_arm.c',
						'ffmpeg_src/libavcodec/arm/h264cmc_neon.S',
						'ffmpeg_src/libavcodec/arm/h264dsp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/h264dsp_neon.S',
						'ffmpeg_src/libavcodec/arm/h264idct_neon.S',
						'ffmpeg_src/libavcodec/arm/h264pred_init_arm.c',
						'ffmpeg_src/libavcodec/arm/h264pred_neon.S',
						'ffmpeg_src/libavcodec/arm/h264qpel_init_arm.c',
						'ffmpeg_src/libavcodec/arm/h264qpel_neon.S',
						'ffmpeg_src/libavcodec/arm/hevcdsp_arm.h',
						'ffmpeg_src/libavcodec/arm/hevcdsp_deblock_neon.S',
						'ffmpeg_src/libavcodec/arm/hevcdsp_idct_neon.S',
						'ffmpeg_src/libavcodec/arm/hevcdsp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/hevcdsp_init_neon.c',
						'ffmpeg_src/libavcodec/arm/hevcdsp_qpel_neon.S',
						'ffmpeg_src/libavcodec/arm/hpeldsp_arm.h',
						'ffmpeg_src/libavcodec/arm/hpeldsp_arm.S',
						'ffmpeg_src/libavcodec/arm/hpeldsp_armv6.S',
						'ffmpeg_src/libavcodec/arm/hpeldsp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/hpeldsp_init_armv6.c',
						'ffmpeg_src/libavcodec/arm/hpeldsp_init_neon.c',
						'ffmpeg_src/libavcodec/arm/hpeldsp_neon.S',
						'ffmpeg_src/libavcodec/arm/idct.h',
						'ffmpeg_src/libavcodec/arm/idctdsp_arm.h',
						'ffmpeg_src/libavcodec/arm/idctdsp_arm.S',
						'ffmpeg_src/libavcodec/arm/idctdsp_armv6.S',
						'ffmpeg_src/libavcodec/arm/idctdsp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/idctdsp_init_armv5te.c',
						'ffmpeg_src/libavcodec/arm/idctdsp_init_armv6.c',
						'ffmpeg_src/libavcodec/arm/idctdsp_init_neon.c',
						'ffmpeg_src/libavcodec/arm/idctdsp_neon.S',
						'ffmpeg_src/libavcodec/arm/int_neon.S',
						'ffmpeg_src/libavcodec/arm/jrevdct_arm.S',
						'ffmpeg_src/libavcodec/arm/lossless_audiodsp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/lossless_audiodsp_neon.S',
						'ffmpeg_src/libavcodec/arm/mathops.h',
						'ffmpeg_src/libavcodec/arm/mdct_fixed_neon.S',
						'ffmpeg_src/libavcodec/arm/mdct_neon.S',
						'ffmpeg_src/libavcodec/arm/mdct_vfp.S',
						'ffmpeg_src/libavcodec/arm/me_cmp_armv6.S',
						'ffmpeg_src/libavcodec/arm/me_cmp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/mlpdsp_armv5te.S',
						'ffmpeg_src/libavcodec/arm/mlpdsp_armv6.S',
						'ffmpeg_src/libavcodec/arm/mlpdsp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/mpegaudiodsp_fixed_armv6.S',
						'ffmpeg_src/libavcodec/arm/mpegaudiodsp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/mpegvideoencdsp_armv6.S',
						'ffmpeg_src/libavcodec/arm/mpegvideoencdsp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/mpegvideo_arm.c',
						'ffmpeg_src/libavcodec/arm/mpegvideo_arm.h',
						'ffmpeg_src/libavcodec/arm/mpegvideo_armv5te.c',
						'ffmpeg_src/libavcodec/arm/mpegvideo_armv5te_s.S',
						'ffmpeg_src/libavcodec/arm/mpegvideo_neon.S',
						'ffmpeg_src/libavcodec/arm/neon.S',
						#'ffmpeg_src/libavcodec/arm/neontest.c',
						'ffmpeg_src/libavcodec/arm/pixblockdsp_armv6.S',
						'ffmpeg_src/libavcodec/arm/pixblockdsp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/rdft_neon.S',
						'ffmpeg_src/libavcodec/arm/rv34dsp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/rv34dsp_neon.S',
						'ffmpeg_src/libavcodec/arm/rv40dsp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/rv40dsp_neon.S',
						'ffmpeg_src/libavcodec/arm/sbrdsp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/sbrdsp_neon.S',
						'ffmpeg_src/libavcodec/arm/simple_idct_arm.S',
						'ffmpeg_src/libavcodec/arm/simple_idct_armv5te.S',
						'ffmpeg_src/libavcodec/arm/simple_idct_armv6.S',
						'ffmpeg_src/libavcodec/arm/simple_idct_neon.S',
						'ffmpeg_src/libavcodec/arm/startcode.h',
						'ffmpeg_src/libavcodec/arm/startcode_armv6.S',
						'ffmpeg_src/libavcodec/arm/synth_filter_neon.S',
						'ffmpeg_src/libavcodec/arm/synth_filter_vfp.S',
						'ffmpeg_src/libavcodec/arm/vc1dsp.h',
						'ffmpeg_src/libavcodec/arm/vc1dsp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/vc1dsp_init_neon.c',
						'ffmpeg_src/libavcodec/arm/vc1dsp_neon.S',
						'ffmpeg_src/libavcodec/arm/videodsp_arm.h',
						'ffmpeg_src/libavcodec/arm/videodsp_armv5te.S',
						'ffmpeg_src/libavcodec/arm/videodsp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/videodsp_init_armv5te.c',
						'ffmpeg_src/libavcodec/arm/vorbisdsp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/vorbisdsp_neon.S',
						'ffmpeg_src/libavcodec/arm/vp3dsp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/vp3dsp_neon.S',
						'ffmpeg_src/libavcodec/arm/vp56_arith.h',
						'ffmpeg_src/libavcodec/arm/vp6dsp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/vp6dsp_neon.S',
						'ffmpeg_src/libavcodec/arm/vp8.h',
						'ffmpeg_src/libavcodec/arm/vp8dsp.h',
						'ffmpeg_src/libavcodec/arm/vp8dsp_armv6.S',
						'ffmpeg_src/libavcodec/arm/vp8dsp_init_arm.c',
						'ffmpeg_src/libavcodec/arm/vp8dsp_init_armv6.c',
						'ffmpeg_src/libavcodec/arm/vp8dsp_init_neon.c',
						'ffmpeg_src/libavcodec/arm/vp8dsp_neon.S',
						'ffmpeg_src/libavcodec/arm/vp8_armv6.S',
						'ffmpeg_src/libavcodec/neon/mpegvideo.c',
						
						
						

					]
				}],
				['target_arch in "ia32 x64"',{
					'includes':[
						'yasm_compile.gypi',
					 ],
					 'variables':{
						'yasm_flags':[
							'-I','ffmpeg_src',
							'-I','config/<(OS)/<(target_arch)',
							'-Pconfig.asm',
							'-DPIC=1',
						 ],
					 },
				}],

				['target_arch in "ia32 x64"',{
					
					'sources' : [
						'ffmpeg_src/libavcodec/x86/ac3dsp.asm',
						'ffmpeg_src/libavcodec/x86/ac3dsp_init.c',
						'ffmpeg_src/libavcodec/x86/audiodsp.asm',
						'ffmpeg_src/libavcodec/x86/audiodsp_init.c',
						'ffmpeg_src/libavcodec/x86/blockdsp.asm',
						'ffmpeg_src/libavcodec/x86/blockdsp_init.c',
						'ffmpeg_src/libavcodec/x86/bswapdsp.asm',
						'ffmpeg_src/libavcodec/x86/bswapdsp_init.c',
						'ffmpeg_src/libavcodec/x86/cabac.h',
						'ffmpeg_src/libavcodec/x86/cavsdsp.c',
						'ffmpeg_src/libavcodec/x86/constants.c',
						'ffmpeg_src/libavcodec/x86/constants.h',
						'ffmpeg_src/libavcodec/x86/dcadsp.asm',
						'ffmpeg_src/libavcodec/x86/dcadsp_init.c',
						#'ffmpeg_src/libavcodec/x86/dct-test.c',
						'ffmpeg_src/libavcodec/x86/dct32.asm',
						'ffmpeg_src/libavcodec/x86/dct_init.c',
						'ffmpeg_src/libavcodec/x86/deinterlace.asm',
						'ffmpeg_src/libavcodec/x86/diracdsp_mmx.c',
						'ffmpeg_src/libavcodec/x86/diracdsp_mmx.h',
						'ffmpeg_src/libavcodec/x86/diracdsp_yasm.asm',
						'ffmpeg_src/libavcodec/x86/dirac_dwt.c',
						'ffmpeg_src/libavcodec/x86/dirac_dwt.h',
						'ffmpeg_src/libavcodec/x86/dnxhdenc.asm',
						'ffmpeg_src/libavcodec/x86/dnxhdenc_init.c',
						'ffmpeg_src/libavcodec/x86/dwt_yasm.asm',
						'ffmpeg_src/libavcodec/x86/fdct.c',
						'ffmpeg_src/libavcodec/x86/fdct.h',
						'ffmpeg_src/libavcodec/x86/fdctdsp_init.c',
						'ffmpeg_src/libavcodec/x86/fft.asm',
						'ffmpeg_src/libavcodec/x86/fft.h',
						'ffmpeg_src/libavcodec/x86/fft_init.c',
						'ffmpeg_src/libavcodec/x86/flacdsp.asm',
						'ffmpeg_src/libavcodec/x86/flacdsp_init.c',
						'ffmpeg_src/libavcodec/x86/flac_dsp_gpl.asm',
						'ffmpeg_src/libavcodec/x86/fmtconvert.asm',
						'ffmpeg_src/libavcodec/x86/fmtconvert_init.c',
						'ffmpeg_src/libavcodec/x86/fpel.asm',
						'ffmpeg_src/libavcodec/x86/fpel.h',
						'ffmpeg_src/libavcodec/x86/g722dsp.asm',
						'ffmpeg_src/libavcodec/x86/g722dsp_init.c',
						'ffmpeg_src/libavcodec/x86/h263dsp_init.c',
						'ffmpeg_src/libavcodec/x86/h263_loopfilter.asm',
						'ffmpeg_src/libavcodec/x86/h264chroma_init.c',
						'ffmpeg_src/libavcodec/x86/h264dsp_init.c',
						'ffmpeg_src/libavcodec/x86/h264_chromamc.asm',
						'ffmpeg_src/libavcodec/x86/h264_chromamc_10bit.asm',
						'ffmpeg_src/libavcodec/x86/h264_deblock.asm',
						'ffmpeg_src/libavcodec/x86/h264_deblock_10bit.asm',
						'ffmpeg_src/libavcodec/x86/h264_i386.h',
						'ffmpeg_src/libavcodec/x86/h264_idct.asm',
						'ffmpeg_src/libavcodec/x86/h264_idct_10bit.asm',
						'ffmpeg_src/libavcodec/x86/h264_intrapred.asm',
						'ffmpeg_src/libavcodec/x86/h264_intrapred_10bit.asm',
						'ffmpeg_src/libavcodec/x86/h264_intrapred_init.c',
						'ffmpeg_src/libavcodec/x86/h264_qpel.c',
						'ffmpeg_src/libavcodec/x86/h264_qpel_10bit.asm',
						'ffmpeg_src/libavcodec/x86/h264_qpel_8bit.asm',
						'ffmpeg_src/libavcodec/x86/h264_weight.asm',
						'ffmpeg_src/libavcodec/x86/h264_weight_10bit.asm',
						'ffmpeg_src/libavcodec/x86/hevcdsp.h',
						'ffmpeg_src/libavcodec/x86/hevcdsp_init.c',
						'ffmpeg_src/libavcodec/x86/hevc_deblock.asm',
						'ffmpeg_src/libavcodec/x86/hevc_idct.asm',
						'ffmpeg_src/libavcodec/x86/hevc_mc.asm',
						'ffmpeg_src/libavcodec/x86/hevc_res_add.asm',
						'ffmpeg_src/libavcodec/x86/hevc_sao.asm',
						'ffmpeg_src/libavcodec/x86/hpeldsp.asm',
						'ffmpeg_src/libavcodec/x86/hpeldsp.h',
						'ffmpeg_src/libavcodec/x86/hpeldsp_init.c',
						#'ffmpeg_src/libavcodec/x86/hpeldsp_rnd_template.c',
						'ffmpeg_src/libavcodec/x86/huffyuvdsp.asm',
						'ffmpeg_src/libavcodec/x86/huffyuvdsp_init.c',
						'ffmpeg_src/libavcodec/x86/huffyuvencdsp_mmx.c',
						'ffmpeg_src/libavcodec/x86/idctdsp.asm',
						'ffmpeg_src/libavcodec/x86/idctdsp.h',
						'ffmpeg_src/libavcodec/x86/idctdsp_init.c',
						'ffmpeg_src/libavcodec/x86/imdct36.asm',
						'ffmpeg_src/libavcodec/x86/inline_asm.h',
						'ffmpeg_src/libavcodec/x86/lossless_audiodsp.asm',
						'ffmpeg_src/libavcodec/x86/lossless_audiodsp_init.c',
						'ffmpeg_src/libavcodec/x86/lossless_videodsp.asm',
						'ffmpeg_src/libavcodec/x86/lossless_videodsp_init.c',
						'ffmpeg_src/libavcodec/x86/lpc.c',
						'ffmpeg_src/libavcodec/x86/mathops.h',
						'ffmpeg_src/libavcodec/x86/me_cmp.asm',
						'ffmpeg_src/libavcodec/x86/me_cmp_init.c',
						'ffmpeg_src/libavcodec/x86/mlpdsp.asm',
						'ffmpeg_src/libavcodec/x86/mlpdsp_init.c',
						'ffmpeg_src/libavcodec/x86/mpegaudiodsp.c',
						'ffmpeg_src/libavcodec/x86/mpegvideo.c',
						'ffmpeg_src/libavcodec/x86/mpegvideodsp.c',
						'ffmpeg_src/libavcodec/x86/mpegvideoenc.c',
						'ffmpeg_src/libavcodec/x86/mpegvideoencdsp.asm',
						'ffmpeg_src/libavcodec/x86/mpegvideoencdsp_init.c',
						#'ffmpeg_src/libavcodec/x86/mpegvideoenc_qns_template.c',
						#'ffmpeg_src/libavcodec/x86/mpegvideoenc_template.c',
						'ffmpeg_src/libavcodec/x86/pixblockdsp.asm',
						'ffmpeg_src/libavcodec/x86/pixblockdsp_init.c',
						'ffmpeg_src/libavcodec/x86/pngdsp.asm',
						'ffmpeg_src/libavcodec/x86/pngdsp_init.c',
						'ffmpeg_src/libavcodec/x86/proresdsp.asm',
						'ffmpeg_src/libavcodec/x86/proresdsp_init.c',
						'ffmpeg_src/libavcodec/x86/qpel.asm',
						'ffmpeg_src/libavcodec/x86/qpeldsp.asm',
						'ffmpeg_src/libavcodec/x86/qpeldsp_init.c',
						#'ffmpeg_src/libavcodec/x86/rnd_template.c',
						'ffmpeg_src/libavcodec/x86/rv34dsp.asm',
						'ffmpeg_src/libavcodec/x86/rv34dsp_init.c',
						'ffmpeg_src/libavcodec/x86/rv40dsp.asm',
						'ffmpeg_src/libavcodec/x86/rv40dsp_init.c',
						'ffmpeg_src/libavcodec/x86/sbrdsp.asm',
						'ffmpeg_src/libavcodec/x86/sbrdsp_init.c',
						'ffmpeg_src/libavcodec/x86/simple_idct.c',
						'ffmpeg_src/libavcodec/x86/simple_idct.h',
						'ffmpeg_src/libavcodec/x86/snowdsp.c',
						'ffmpeg_src/libavcodec/x86/svq1enc.asm',
						'ffmpeg_src/libavcodec/x86/svq1enc_init.c',
						'ffmpeg_src/libavcodec/x86/ttadsp.asm',
						'ffmpeg_src/libavcodec/x86/ttadsp_init.c',
						'ffmpeg_src/libavcodec/x86/v210-init.c',
						'ffmpeg_src/libavcodec/x86/v210.asm',
						'ffmpeg_src/libavcodec/x86/v210enc.asm',
						'ffmpeg_src/libavcodec/x86/v210enc_init.c',
						'ffmpeg_src/libavcodec/x86/vc1dsp.asm',
						'ffmpeg_src/libavcodec/x86/vc1dsp.h',
						'ffmpeg_src/libavcodec/x86/vc1dsp_init.c',
						'ffmpeg_src/libavcodec/x86/vc1dsp_mmx.c',
						'ffmpeg_src/libavcodec/x86/videodsp.asm',
						'ffmpeg_src/libavcodec/x86/videodsp_init.c',
						'ffmpeg_src/libavcodec/x86/vorbisdsp.asm',
						'ffmpeg_src/libavcodec/x86/vorbisdsp_init.c',
						'ffmpeg_src/libavcodec/x86/vp3dsp.asm',
						'ffmpeg_src/libavcodec/x86/vp3dsp_init.c',
						'ffmpeg_src/libavcodec/x86/vp56_arith.h',
						'ffmpeg_src/libavcodec/x86/vp6dsp.asm',
						'ffmpeg_src/libavcodec/x86/vp6dsp_init.c',
						'ffmpeg_src/libavcodec/x86/vp8dsp.asm',
						'ffmpeg_src/libavcodec/x86/vp8dsp_init.c',
						'ffmpeg_src/libavcodec/x86/vp8dsp_loopfilter.asm',
						'ffmpeg_src/libavcodec/x86/vp9dsp_init.c',
						'ffmpeg_src/libavcodec/x86/vp9intrapred.asm',
						'ffmpeg_src/libavcodec/x86/vp9itxfm.asm',
						'ffmpeg_src/libavcodec/x86/vp9lpf.asm',
						'ffmpeg_src/libavcodec/x86/vp9mc.asm',
						#'ffmpeg_src/libavcodec/x86/w64xmmtest.c',
						'ffmpeg_src/libavcodec/x86/xvididct.h',
						'ffmpeg_src/libavcodec/x86/xvididct_init.c',
						'ffmpeg_src/libavcodec/x86/xvididct_mmx.c',
						'ffmpeg_src/libavcodec/x86/xvididct_sse2.c',					
						
					]
				}],
				['OS=="linux"',{
					'cflags':[
						'-fvisibility=hidden',
					],
				}],
				[ 'OS in "linux android"', {
					'sources':[
					],
					'link_settings': {
						'libraries': [
							'-lz'
						],
					},
				}],
				['OS == "win"',{
					'dependencies':[
						'<!@(nnbu-dependency --dependency zlib)',
					],
					'include_dirs':[
						'<!@(nnbu-dependency --headers zlib)',
					],
					'link_settings':{
						'libraries':[
							'<!@(nnbu-dependency --lib-fix --libs zlib)',
						],
					},
				}],
			]
		}
		,{
			'target_name': 'avdevice',
			'type':'<(primary_libraries)',
			'dependencies':[
				'avutil',
				'avcodec',
				'avfilter',
				'avformat',
			],
			'defines':[
				'_POSIX_SOURCE',
			],
			'include_dirs':[
				'libavdevice',
				'ffmpeg_src',
				'ffmpeg_src/libavdevice',
			],
			'direct_dependent_settings': {
				'include_dirs': [
					'ffmpeg_src/libavdevice',
				],
				'conditions':[
					['OS == "win"',{
						'link_settings': {
							'libraries': [
								'-lOle32.lib',
								'-lStrmiids.lib'
							]
						 },
					}]
				],
				
			 },
			'sources':[
				'definitions/avdevice.def',
				'ffmpeg_src/libavdevice/alldevices.c',
				'ffmpeg_src/libavdevice/avdevice.c',
				'ffmpeg_src/libavdevice/file_open.c',
				'ffmpeg_src/libavdevice/lavfi.c',
				'ffmpeg_src/libavdevice/timefilter.c',
				'ffmpeg_src/libavdevice/utils.c',
				
				
			],
			'conditions':[
				['OS == "linux"',{
					'cflags':[
						'-include sys/time.h',
					],		
				}],
				['OS in "linux android"',{
					'dependencies':[
						'<!@(nnbu-dependency --dependency alsa-lib)',
						#'../alsa-lib.module/alsa-lib.gyp:alsa-lib',
					],
								
					'sources':[
						'ffmpeg_src/libavdevice/dv1394.c',
						#'ffmpeg_src/libavdevice/fbdev_common.c',
						#'ffmpeg_src/libavdevice/fbdev_dec.c',
						#'ffmpeg_src/libavdevice/fbdev_enc.c',
						'ffmpeg_src/libavdevice/v4l2-common.c',
						'ffmpeg_src/libavdevice/v4l2.c',
						'ffmpeg_src/libavdevice/v4l2enc.c',
						'ffmpeg_src/libavdevice/alsa-audio-common.c',
						'ffmpeg_src/libavdevice/alsa-audio-dec.c',
						'ffmpeg_src/libavdevice/alsa-audio-enc.c',
						'ffmpeg_src/libavdevice/alsa-audio.h',
						
					
					],
				}],
				['OS == "win"',{
					'link_settings': {
						'libraries': [
							'-lOle32.lib',
							'-lOleAut32.lib',
							'-lStrmiids.lib'
						]
					 },
					'sources':[
						'ffmpeg_src/libavdevice/dshow.c',
						'ffmpeg_src/libavdevice/dshow_capture.h',
						'ffmpeg_src/libavdevice/dshow_common.c',
						'ffmpeg_src/libavdevice/dshow_enummediatypes.c',
						'ffmpeg_src/libavdevice/dshow_enumpins.c',
						'ffmpeg_src/libavdevice/dshow_filter.c',
						'ffmpeg_src/libavdevice/dshow_pin.c',	
						'ffmpeg_src/libavdevice/dshow_crossbar.c',
					],
				}],
			]
		}

		,{
			'target_name': 'avfilter',
			'type':'<(primary_libraries)',
			'dependencies':[
				'avutil',
				'swscale',
				'swresample',
				'avresample',
				'postproc',
				'avcodec',
				'avformat',
			],
			'defines':[],
			'include_dirs':[
				'ffmpeg_src',
				'ffmpeg_src/libavfilter',
			],
			'direct_dependent_settings': {
				'include_dirs': [
					'ffmpeg_src/libavfilter',
				],
			 },
			 'export_dependent_settings':[
				'swscale'
			 ],
			'sources':[
				'definitions/avfilter.def',
				'ffmpeg_src/libavfilter/aeval.c',
				#'ffmpeg_src/libavfilter/af_aconvert.c',
				'ffmpeg_src/libavfilter/af_adelay.c',
				'ffmpeg_src/libavfilter/af_aecho.c',
				'ffmpeg_src/libavfilter/af_afade.c',
				'ffmpeg_src/libavfilter/af_aformat.c',
				'ffmpeg_src/libavfilter/af_amerge.c',
				'ffmpeg_src/libavfilter/af_amix.c',
				'ffmpeg_src/libavfilter/af_anull.c',
				'ffmpeg_src/libavfilter/af_apad.c',
				'ffmpeg_src/libavfilter/af_aphaser.c',
				'ffmpeg_src/libavfilter/af_aresample.c',
				'ffmpeg_src/libavfilter/af_asetnsamples.c',
				'ffmpeg_src/libavfilter/af_asetrate.c',
				'ffmpeg_src/libavfilter/af_ashowinfo.c',
				'ffmpeg_src/libavfilter/af_astats.c',
				'ffmpeg_src/libavfilter/af_astreamsync.c',
				'ffmpeg_src/libavfilter/af_asyncts.c',
				'ffmpeg_src/libavfilter/af_atempo.c',
				'ffmpeg_src/libavfilter/af_biquads.c',
				'ffmpeg_src/libavfilter/af_channelmap.c',
				'ffmpeg_src/libavfilter/af_channelsplit.c',
				'ffmpeg_src/libavfilter/af_compand.c',
				'ffmpeg_src/libavfilter/af_earwax.c',
				'ffmpeg_src/libavfilter/af_join.c',
				'ffmpeg_src/libavfilter/af_pan.c',
				'ffmpeg_src/libavfilter/af_replaygain.c',
				'ffmpeg_src/libavfilter/af_resample.c',
				'ffmpeg_src/libavfilter/af_silencedetect.c',
				'ffmpeg_src/libavfilter/af_volume.c',
				'ffmpeg_src/libavfilter/af_volumedetect.c',
				'ffmpeg_src/libavfilter/allfilters.c',
				'ffmpeg_src/libavfilter/asink_anullsink.c',
				'ffmpeg_src/libavfilter/asrc_anullsrc.c',
				'ffmpeg_src/libavfilter/asrc_sine.c',
				'ffmpeg_src/libavfilter/audio.c',
				'ffmpeg_src/libavfilter/avcodec.c',
				'ffmpeg_src/libavfilter/avfilter.c',
				'ffmpeg_src/libavfilter/avfiltergraph.c',
				'ffmpeg_src/libavfilter/avf_avectorscope.c',
				'ffmpeg_src/libavfilter/avf_concat.c',
				'ffmpeg_src/libavfilter/avf_showspectrum.c',
				'ffmpeg_src/libavfilter/avf_showwaves.c',
				'ffmpeg_src/libavfilter/bbox.c',
				'ffmpeg_src/libavfilter/buffer.c',
				'ffmpeg_src/libavfilter/buffersink.c',
				'ffmpeg_src/libavfilter/buffersrc.c',
				'ffmpeg_src/libavfilter/drawutils.c',
				'ffmpeg_src/libavfilter/dualinput.c',
				'ffmpeg_src/libavfilter/fifo.c',
				'ffmpeg_src/libavfilter/filtfmts.c',
				'ffmpeg_src/libavfilter/formats.c',
				'ffmpeg_src/libavfilter/framesync.c',
				
				'ffmpeg_src/libavfilter/f_interleave.c',
				'ffmpeg_src/libavfilter/f_perms.c',
				'ffmpeg_src/libavfilter/f_select.c',
				'ffmpeg_src/libavfilter/f_sendcmd.c',
				'ffmpeg_src/libavfilter/graphdump.c',
				'ffmpeg_src/libavfilter/graphparser.c',
				'ffmpeg_src/libavfilter/lavfutils.c',
				'ffmpeg_src/libavfilter/lswsutils.c',
				'ffmpeg_src/libavfilter/pthread.c',
				'ffmpeg_src/libavfilter/setpts.c',
				'ffmpeg_src/libavfilter/settb.c',
				'ffmpeg_src/libavfilter/split.c',
				'ffmpeg_src/libavfilter/src_movie.c',
				'ffmpeg_src/libavfilter/transform.c',
				'ffmpeg_src/libavfilter/trim.c',
				'ffmpeg_src/libavfilter/vf_alphamerge.c',
				'ffmpeg_src/libavfilter/vf_aspect.c',
				'ffmpeg_src/libavfilter/vf_bbox.c',
				'ffmpeg_src/libavfilter/vf_blackdetect.c',
				
				'ffmpeg_src/libavfilter/vf_blend.c',
				
				'ffmpeg_src/libavfilter/vf_colorbalance.c',
				'ffmpeg_src/libavfilter/vf_colorchannelmixer.c',
				
				'ffmpeg_src/libavfilter/vf_copy.c',
				'ffmpeg_src/libavfilter/vf_crop.c',
				
				'ffmpeg_src/libavfilter/vf_curves.c',
				'ffmpeg_src/libavfilter/vf_dctdnoiz.c',
				'ffmpeg_src/libavfilter/vf_decimate.c',
				'ffmpeg_src/libavfilter/vf_dejudder.c',
				
				'ffmpeg_src/libavfilter/vf_deshake.c',
				'ffmpeg_src/libavfilter/vf_drawbox.c',
				'ffmpeg_src/libavfilter/vf_edgedetect.c',
				'ffmpeg_src/libavfilter/vf_elbg.c',
				'ffmpeg_src/libavfilter/vf_extractplanes.c',
				'ffmpeg_src/libavfilter/vf_fade.c',
				'ffmpeg_src/libavfilter/vf_field.c',
				'ffmpeg_src/libavfilter/vf_fieldmatch.c',
				'ffmpeg_src/libavfilter/vf_fieldorder.c',
				'ffmpeg_src/libavfilter/vf_format.c',
				'ffmpeg_src/libavfilter/vf_fps.c',
				'ffmpeg_src/libavfilter/vf_framepack.c',
				'ffmpeg_src/libavfilter/vf_framestep.c',
				
				'ffmpeg_src/libavfilter/vf_gradfun.c',
				'ffmpeg_src/libavfilter/vf_hflip.c',
				
				'ffmpeg_src/libavfilter/vf_histogram.c',
				
				'ffmpeg_src/libavfilter/vf_hue.c',
				'ffmpeg_src/libavfilter/vf_idet.c',
				'ffmpeg_src/libavfilter/vf_il.c',
				
				
				'ffmpeg_src/libavfilter/vf_lut.c',
				'ffmpeg_src/libavfilter/vf_lut3d.c',
				
				'ffmpeg_src/libavfilter/vf_mergeplanes.c',
				#'ffmpeg_src/libavfilter/vf_mp.c',
				
				'ffmpeg_src/libavfilter/vf_noise.c',
				'ffmpeg_src/libavfilter/vf_null.c',
				'ffmpeg_src/libavfilter/vf_overlay.c',
				
				'ffmpeg_src/libavfilter/vf_pad.c',
				
				
				
				'ffmpeg_src/libavfilter/vf_psnr.c',
				
				'ffmpeg_src/libavfilter/vf_removelogo.c',
				'ffmpeg_src/libavfilter/vf_rotate.c',
				
				'ffmpeg_src/libavfilter/vf_scale.c',
				'ffmpeg_src/libavfilter/vf_separatefields.c',
				'ffmpeg_src/libavfilter/vf_setfield.c',
				'ffmpeg_src/libavfilter/vf_showinfo.c',
				'ffmpeg_src/libavfilter/vf_shuffleplanes.c',
				
				
				
				
				'ffmpeg_src/libavfilter/vf_swapuv.c',
				'ffmpeg_src/libavfilter/vf_telecine.c',
				'ffmpeg_src/libavfilter/vf_thumbnail.c',
				'ffmpeg_src/libavfilter/vf_tile.c',
				
				'ffmpeg_src/libavfilter/vf_transpose.c',
				'ffmpeg_src/libavfilter/vf_unsharp.c',
				'ffmpeg_src/libavfilter/vf_vflip.c',
				'ffmpeg_src/libavfilter/vf_vignette.c',
				'ffmpeg_src/libavfilter/vf_w3fdif.c',
				'ffmpeg_src/libavfilter/vf_yadif.c',
				'ffmpeg_src/libavfilter/video.c',
				'ffmpeg_src/libavfilter/vsink_nullsink.c',
				'ffmpeg_src/libavfilter/vsrc_cellauto.c',
				'ffmpeg_src/libavfilter/vsrc_life.c',
				'ffmpeg_src/libavfilter/vsrc_mandelbrot.c',
				'ffmpeg_src/libavfilter/opencl_allkernels.c',
				#'ffmpeg_src/libavfilter/libmpcodecs/img_format.c',
				#'ffmpeg_src/libavfilter/libmpcodecs/mp_image.c',
				#'ffmpeg_src/libavfilter/libmpcodecs/vf_eq.c',
				#'ffmpeg_src/libavfilter/libmpcodecs/vf_eq2.c',
				#'ffmpeg_src/libavfilter/libmpcodecs/vf_fspp.c',
				#'ffmpeg_src/libavfilter/libmpcodecs/vf_ilpack.c',
				#'ffmpeg_src/libavfilter/libmpcodecs/vf_pp7.c',
				#'ffmpeg_src/libavfilter/libmpcodecs/vf_softpulldown.c',
				#'ffmpeg_src/libavfilter/libmpcodecs/vf_uspp.c',
				#'ffmpeg_src/libavfilter/af_bs2b.c',
				'ffmpeg_src/libavfilter/af_dcshift.c',
				'ffmpeg_src/libavfilter/af_flanger.c',
				'ffmpeg_src/libavfilter/af_silenceremove.c',
				'ffmpeg_src/libavfilter/vf_codecview.c',
				'ffmpeg_src/libavfilter/vf_colorlevels.c',
				
				
				'ffmpeg_src/libavfilter/vf_hqx.c',
				'ffmpeg_src/libavfilter/vf_lenscorrection.c',
				'ffmpeg_src/libavfilter/vf_palettegen.c',
				'ffmpeg_src/libavfilter/vf_paletteuse.c',
				
				'ffmpeg_src/libavfilter/vf_qp.c',
				
				'ffmpeg_src/libavfilter/vf_showpalette.c',
				'ffmpeg_src/libavfilter/vf_signalstats.c',
				
				'ffmpeg_src/libavfilter/vf_xbr.c',
				'ffmpeg_src/libavfilter/vf_zoompan.c',
				'ffmpeg_src/libavfilter/avf_showcqt.c',
				'ffmpeg_src/libavfilter/generate_wave_table.c',
				
				
				
			],
			'conditions':[
				['use_gpl_components == 1',{
					'sources':[
						'ffmpeg_src/libavfilter/vf_blackframe.c',
						'ffmpeg_src/libavfilter/f_ebur128.c',
						'ffmpeg_src/libavfilter/vf_boxblur.c',
						'ffmpeg_src/libavfilter/vf_colormatrix.c',
						'ffmpeg_src/libavfilter/vf_cropdetect.c',
						'ffmpeg_src/libavfilter/vf_delogo.c',
						'ffmpeg_src/libavfilter/vf_eq.c',
						'ffmpeg_src/libavfilter/vf_fspp.c',
						'ffmpeg_src/libavfilter/vf_geq.c',
						'ffmpeg_src/libavfilter/vf_histeq.c',
						'ffmpeg_src/libavfilter/vf_hqdn3d.c',
						'ffmpeg_src/libavfilter/vf_interlace.c',
						'ffmpeg_src/libavfilter/vf_kerndeint.c',
						'ffmpeg_src/libavfilter/vf_mcdeint.c',
						'ffmpeg_src/libavfilter/vf_mpdecimate.c',
						'ffmpeg_src/libavfilter/vf_owdenoise.c',
						'ffmpeg_src/libavfilter/vf_perspective.c',
						'ffmpeg_src/libavfilter/vf_phase.c',
						'ffmpeg_src/libavfilter/vf_pp.c',
						'ffmpeg_src/libavfilter/vf_pp7.c',
						'ffmpeg_src/libavfilter/vf_pullup.c',
						'ffmpeg_src/libavfilter/vf_sab.c',
						'ffmpeg_src/libavfilter/vf_smartblur.c',
						'ffmpeg_src/libavfilter/vf_repeatfields.c',
						'ffmpeg_src/libavfilter/vf_spp.c',
						'ffmpeg_src/libavfilter/vf_stereo3d.c',
						'ffmpeg_src/libavfilter/vf_super2xsai.c',
						'ffmpeg_src/libavfilter/vf_tinterlace.c',
						'ffmpeg_src/libavfilter/vf_uspp.c',
					],
				}],
				
				['target_arch in "ia32 x64"',{
					'includes':[
						'yasm_compile.gypi',
					 ],
					 'variables':{
						'yasm_flags':[
							'-I','ffmpeg_src',
							'-I','config/<(OS)/<(target_arch)',
							'-Pconfig.asm',
							'-DPIC=1',
						 ],
					 },
				}],
				
				['target_arch in "ia32 x64"',{
					'sources':[
						'ffmpeg_src/libavfilter/x86/af_volume.asm',
						'ffmpeg_src/libavfilter/x86/af_volume_init.c',
						'ffmpeg_src/libavfilter/x86/vf_fspp.asm',
						'ffmpeg_src/libavfilter/x86/vf_fspp_init.c',
						'ffmpeg_src/libavfilter/x86/vf_gradfun.asm',
						'ffmpeg_src/libavfilter/x86/vf_gradfun_init.c',
						'ffmpeg_src/libavfilter/x86/vf_hqdn3d.asm',
						'ffmpeg_src/libavfilter/x86/vf_hqdn3d_init.c',
						'ffmpeg_src/libavfilter/x86/vf_idet.asm',
						'ffmpeg_src/libavfilter/x86/vf_idet_init.c',
						'ffmpeg_src/libavfilter/x86/vf_interlace.asm',
						'ffmpeg_src/libavfilter/x86/vf_interlace_init.c',
						'ffmpeg_src/libavfilter/x86/vf_noise.c',
						'ffmpeg_src/libavfilter/x86/vf_pp7.asm',
						'ffmpeg_src/libavfilter/x86/vf_pp7_init.c',
						'ffmpeg_src/libavfilter/x86/vf_pullup.asm',
						'ffmpeg_src/libavfilter/x86/vf_pullup_init.c',
						'ffmpeg_src/libavfilter/x86/vf_tinterlace_init.c',
						'ffmpeg_src/libavfilter/x86/vf_yadif.asm',
						'ffmpeg_src/libavfilter/x86/vf_yadif_init.c',
						'ffmpeg_src/libavfilter/x86/yadif-10.asm',
						'ffmpeg_src/libavfilter/x86/yadif-16.asm',
					],
					
				}],
				['target_arch in "ia32 x64" and use_gpl_components == 1',{
					'sources':[
						'ffmpeg_src/libavfilter/x86/vf_eq.c',
						'ffmpeg_src/libavfilter/x86/vf_spp.c',
					]
				}],
			]
		}

		,{
			'target_name':'avformat',
			'type':'<(primary_libraries)',
			'direct_dependent_settings': {
				'include_dirs': [
					'ffmpeg_src/libavformat',
				],
			 },
			 'dependencies':[
				'avformat_p1',
				'avformat_p2',
				'avutil',
			 ],
			 'sources':[
				'definitions/avformat.def',
				'ffmpeg_src/libavformat/allformats.c',
			 ],
			 'conditions':[
				 [ 'OS in "linux"', {
						'sources':[
						],
						'link_settings': {
							'libraries': [
								'-ldl',
							],
						},
					}],
			],
		}
		
		,{
			'target_name': 'avformat_p1',
			'type':'<(library)',
			'dependencies':[
				'avcodec',
			],
			'defines':[],
			'include_dirs':[
				'ffmpeg_src',
				'ffmpeg_src/libavformat',
			],
			'direct_dependent_settings': {
				'include_dirs': [
					'ffmpeg_src/libavformat',
				],
			 },
			 'export_dependent_settings':[
				'avcodec',
			 ],
			'sources':[
				'ffmpeg_src/libavformat/4xm.c',
				'ffmpeg_src/libavformat/a64.c',
				'ffmpeg_src/libavformat/aacdec.c',
				'ffmpeg_src/libavformat/ac3dec.c',
				'ffmpeg_src/libavformat/act.c',
				'ffmpeg_src/libavformat/adp.c',
				'ffmpeg_src/libavformat/adtsenc.c',
				'ffmpeg_src/libavformat/adxdec.c',
				'ffmpeg_src/libavformat/aea.c',
				'ffmpeg_src/libavformat/afc.c',
				'ffmpeg_src/libavformat/aiffdec.c',
				'ffmpeg_src/libavformat/aiffenc.c',
				
				'ffmpeg_src/libavformat/amr.c',
				'ffmpeg_src/libavformat/anm.c',
				'ffmpeg_src/libavformat/apc.c',
				'ffmpeg_src/libavformat/ape.c',
				'ffmpeg_src/libavformat/apetag.c',
				'ffmpeg_src/libavformat/aqtitledec.c',
				'ffmpeg_src/libavformat/asf.c',
				'ffmpeg_src/libavformat/asfcrypt.c',
				'ffmpeg_src/libavformat/asfdec.c',
				'ffmpeg_src/libavformat/asfenc.c',
				'ffmpeg_src/libavformat/assdec.c',
				'ffmpeg_src/libavformat/assenc.c',
				'ffmpeg_src/libavformat/ast.c',
				'ffmpeg_src/libavformat/astdec.c',
				'ffmpeg_src/libavformat/astenc.c',
				'ffmpeg_src/libavformat/au.c',
				'ffmpeg_src/libavformat/audiointerleave.c',
				'ffmpeg_src/libavformat/avc.c',
				'ffmpeg_src/libavformat/avidec.c',
				'ffmpeg_src/libavformat/avienc.c',
				'ffmpeg_src/libavformat/avio.c',
				'ffmpeg_src/libavformat/aviobuf.c',
				'ffmpeg_src/libavformat/avisynth.c',
				'ffmpeg_src/libavformat/avlanguage.c',
				'ffmpeg_src/libavformat/avr.c',
				'ffmpeg_src/libavformat/avs.c',
				'ffmpeg_src/libavformat/bethsoftvid.c',
				'ffmpeg_src/libavformat/bfi.c',
				'ffmpeg_src/libavformat/bink.c',
				'ffmpeg_src/libavformat/bintext.c',
				'ffmpeg_src/libavformat/bit.c',
				'ffmpeg_src/libavformat/bmv.c',
				'ffmpeg_src/libavformat/boadec.c',
				'ffmpeg_src/libavformat/brstm.c',
				'ffmpeg_src/libavformat/c93.c',
				'ffmpeg_src/libavformat/cache.c',
				'ffmpeg_src/libavformat/caf.c',
				'ffmpeg_src/libavformat/cafdec.c',
				'ffmpeg_src/libavformat/cafenc.c',
				'ffmpeg_src/libavformat/cavsvideodec.c',
				'ffmpeg_src/libavformat/cdg.c',
				'ffmpeg_src/libavformat/cdxl.c',
				'ffmpeg_src/libavformat/cinedec.c',
				'ffmpeg_src/libavformat/concat.c',
				'ffmpeg_src/libavformat/concatdec.c',
				'ffmpeg_src/libavformat/crcenc.c',
				'ffmpeg_src/libavformat/crypto.c',
				'ffmpeg_src/libavformat/cutils.c',
				'ffmpeg_src/libavformat/data_uri.c',
				#'ffmpeg_src/libavformat/daud.c',
				'ffmpeg_src/libavformat/dfa.c',
				'ffmpeg_src/libavformat/diracdec.c',
				'ffmpeg_src/libavformat/dnxhddec.c',
				'ffmpeg_src/libavformat/dsicin.c',
				'ffmpeg_src/libavformat/dtsdec.c',
				'ffmpeg_src/libavformat/dtshddec.c',
				'ffmpeg_src/libavformat/dv.c',
				'ffmpeg_src/libavformat/dvenc.c',
				'ffmpeg_src/libavformat/dxa.c',
				'ffmpeg_src/libavformat/eacdata.c',
				'ffmpeg_src/libavformat/electronicarts.c',
				'ffmpeg_src/libavformat/epafdec.c',
				'ffmpeg_src/libavformat/ffmdec.c',
				'ffmpeg_src/libavformat/ffmenc.c',
				'ffmpeg_src/libavformat/ffmetadec.c',
				'ffmpeg_src/libavformat/ffmetaenc.c',
				'ffmpeg_src/libavformat/file.c',
				'ffmpeg_src/libavformat/file_open.c',
				'ffmpeg_src/libavformat/filmstripdec.c',
				'ffmpeg_src/libavformat/filmstripenc.c',
				'ffmpeg_src/libavformat/flacdec.c',
				'ffmpeg_src/libavformat/flacenc.c',
				'ffmpeg_src/libavformat/flacenc_header.c',
				'ffmpeg_src/libavformat/flac_picture.c',
				'ffmpeg_src/libavformat/flic.c',
				'ffmpeg_src/libavformat/flvdec.c',
				'ffmpeg_src/libavformat/flvenc.c',
				'ffmpeg_src/libavformat/format.c',
				'ffmpeg_src/libavformat/framecrcenc.c',
				'ffmpeg_src/libavformat/framehash.c',
				'ffmpeg_src/libavformat/frmdec.c',
				'ffmpeg_src/libavformat/ftp.c',
				'ffmpeg_src/libavformat/g722.c',
				'ffmpeg_src/libavformat/g723_1.c',
				'ffmpeg_src/libavformat/g729dec.c',
				'ffmpeg_src/libavformat/gif.c',
				'ffmpeg_src/libavformat/gifdec.c',
				'ffmpeg_src/libavformat/golomb_tab.c',
				'ffmpeg_src/libavformat/gopher.c',
				'ffmpeg_src/libavformat/gsmdec.c',
				'ffmpeg_src/libavformat/gxf.c',
				'ffmpeg_src/libavformat/gxfenc.c',
				'ffmpeg_src/libavformat/h261dec.c',
				'ffmpeg_src/libavformat/h263dec.c',
				'ffmpeg_src/libavformat/h264dec.c',
				'ffmpeg_src/libavformat/hdsenc.c',
				'ffmpeg_src/libavformat/hevc.c',
				'ffmpeg_src/libavformat/hevcdec.c',
				'ffmpeg_src/libavformat/hls.c',
				'ffmpeg_src/libavformat/hlsenc.c',
				'ffmpeg_src/libavformat/hlsproto.c',
				'ffmpeg_src/libavformat/hnm.c',
				'ffmpeg_src/libavformat/http.c',
				'ffmpeg_src/libavformat/httpauth.c',
				'ffmpeg_src/libavformat/icodec.c',
				'ffmpeg_src/libavformat/icoenc.c',
				'ffmpeg_src/libavformat/id3v1.c',
				'ffmpeg_src/libavformat/id3v2.c',
				'ffmpeg_src/libavformat/id3v2enc.c',
				'ffmpeg_src/libavformat/idcin.c',
				'ffmpeg_src/libavformat/idroqdec.c',
				'ffmpeg_src/libavformat/idroqenc.c',
				'ffmpeg_src/libavformat/iff.c',
				'ffmpeg_src/libavformat/ilbc.c',
				'ffmpeg_src/libavformat/img2.c',
				'ffmpeg_src/libavformat/img2dec.c',
				'ffmpeg_src/libavformat/img2enc.c',
				'ffmpeg_src/libavformat/ingenientdec.c',
				'ffmpeg_src/libavformat/ipmovie.c',
				'ffmpeg_src/libavformat/ircam.c',
				'ffmpeg_src/libavformat/ircamdec.c',
				'ffmpeg_src/libavformat/ircamenc.c',
				'ffmpeg_src/libavformat/isom.c',
				'ffmpeg_src/libavformat/iss.c',
				'ffmpeg_src/libavformat/iv8.c',
				'ffmpeg_src/libavformat/ivfdec.c',
				'ffmpeg_src/libavformat/ivfenc.c',
				'ffmpeg_src/libavformat/jacosubdec.c',
				'ffmpeg_src/libavformat/jacosubenc.c',
				'ffmpeg_src/libavformat/jvdec.c',
				'ffmpeg_src/libavformat/latmenc.c',
				'ffmpeg_src/libavformat/lmlm4.c',
				'ffmpeg_src/libavformat/loasdec.c',
				'ffmpeg_src/libavformat/log2_tab.c',
				'ffmpeg_src/libavformat/lvfdec.c',
				'ffmpeg_src/libavformat/lxfdec.c',
				'ffmpeg_src/libavformat/m4vdec.c',
				'ffmpeg_src/libavformat/matroska.c',
				'ffmpeg_src/libavformat/matroskadec.c',
				'ffmpeg_src/libavformat/matroskaenc.c',
				'ffmpeg_src/libavformat/md5enc.c',
				'ffmpeg_src/libavformat/md5proto.c',
				'ffmpeg_src/libavformat/metadata.c',
				'ffmpeg_src/libavformat/mgsts.c',
				'ffmpeg_src/libavformat/microdvddec.c',
				'ffmpeg_src/libavformat/microdvdenc.c',
				'ffmpeg_src/libavformat/mkvtimestamp_v2.c',
				'ffmpeg_src/libavformat/apngdec.c',
				'ffmpeg_src/libavformat/dashenc.c',
				'ffmpeg_src/libavformat/daudenc.c',
				'ffmpeg_src/libavformat/dauddec.c',
				'ffmpeg_src/libavformat/dss.c',
				'ffmpeg_src/libavformat/lrcenc.c',
				#'ffmpeg_src/libavformat/libsmbclient.c',
				'ffmpeg_src/libavformat/icecast.c',
				'ffmpeg_src/libavformat/yuv4mpegdec.c',
				'ffmpeg_src/libavformat/yuv4mpegenc.c',
				'ffmpeg_src/libavformat/dump.c',
				'ffmpeg_src/libavformat/lrc.c',
				'ffmpeg_src/libavformat/lrcdec.c',
				'ffmpeg_src/libavformat/lrcenc.c',
				#'ffmpeg_src/libavformat/rtpenc_mpegts.c',
				'ffmpeg_src/libavformat/webmdashenc.c',
				'ffmpeg_src/libavformat/stldec.c',
				'ffmpeg_src/libavformat/supdec.c',
				'ffmpeg_src/libavformat/webpenc.c',
				
				
			],
			'conditions':[
				['OS != "win"',{
					'sources':[
						'ffmpeg_src/libavformat/unix.c',
					],
					'link_settings':{
						'libraries':[
							#'-lsocket'
						],
					},
				}],
				['OS == "win"',{
					'link_settings': {
						'libraries': [
							'-lws2_32.lib'
						]
					}
				}]
				
			]
		}
		
				,{
			'target_name': 'avformat_p2',
			'type':'<(library)',
			'dependencies':[
				'avcodec',
			],
			'defines':[],
			'include_dirs':[
				'ffmpeg_src',
				'ffmpeg_src/libavformat',
			],
			'direct_dependent_settings': {
				'include_dirs': [
					'ffmpeg_src/libavformat',
				],
			 },
			 'export_dependent_settings':[
				'avcodec',
			 ],
			'sources':[
				
				'ffmpeg_src/libavformat/mm.c',
				'ffmpeg_src/libavformat/mmf.c',
				'ffmpeg_src/libavformat/mms.c',
				'ffmpeg_src/libavformat/mmsh.c',
				'ffmpeg_src/libavformat/mmst.c',
				'ffmpeg_src/libavformat/mov.c',
				'ffmpeg_src/libavformat/mov_chan.c',
				'ffmpeg_src/libavformat/mp3dec.c',
				'ffmpeg_src/libavformat/mp3enc.c',
				'ffmpeg_src/libavformat/mpc.c',
				'ffmpeg_src/libavformat/mpc8.c',
				'ffmpeg_src/libavformat/mpeg.c',
				'ffmpeg_src/libavformat/mpegenc.c',
				'ffmpeg_src/libavformat/mpegts.c',
				'ffmpeg_src/libavformat/mpegtsenc.c',
				'ffmpeg_src/libavformat/mpegvideodec.c',
				'ffmpeg_src/libavformat/mpjpeg.c',
				'ffmpeg_src/libavformat/mpl2dec.c',
				'ffmpeg_src/libavformat/mpsubdec.c',
				'ffmpeg_src/libavformat/msnwc_tcp.c',
				'ffmpeg_src/libavformat/mtv.c',
				'ffmpeg_src/libavformat/mux.c',
				'ffmpeg_src/libavformat/mvdec.c',
				'ffmpeg_src/libavformat/mvi.c',
				'ffmpeg_src/libavformat/mxf.c',
				'ffmpeg_src/libavformat/mxfdec.c',
				'ffmpeg_src/libavformat/mxfenc.c',
				'ffmpeg_src/libavformat/mxg.c',
				'ffmpeg_src/libavformat/ncdec.c',
				'ffmpeg_src/libavformat/network.c',
				'ffmpeg_src/libavformat/nistspheredec.c',
				'ffmpeg_src/libavformat/nsvdec.c',
				'ffmpeg_src/libavformat/nullenc.c',
				'ffmpeg_src/libavformat/nut.c',
				'ffmpeg_src/libavformat/nutdec.c',
				'ffmpeg_src/libavformat/nutenc.c',
				'ffmpeg_src/libavformat/nuv.c',
				'ffmpeg_src/libavformat/oggdec.c',
				'ffmpeg_src/libavformat/oggenc.c',
				'ffmpeg_src/libavformat/oggparsecelt.c',
				'ffmpeg_src/libavformat/oggparsedirac.c',
				'ffmpeg_src/libavformat/oggparseflac.c',
				'ffmpeg_src/libavformat/oggparseogm.c',
				'ffmpeg_src/libavformat/oggparseopus.c',
				'ffmpeg_src/libavformat/oggparseskeleton.c',
				'ffmpeg_src/libavformat/oggparsespeex.c',
				'ffmpeg_src/libavformat/oggparsetheora.c',
				'ffmpeg_src/libavformat/oggparsevorbis.c',
				'ffmpeg_src/libavformat/oggparsevp8.c',
				'ffmpeg_src/libavformat/oma.c',
				'ffmpeg_src/libavformat/omadec.c',
				'ffmpeg_src/libavformat/omaenc.c',
				'ffmpeg_src/libavformat/options.c',
				'ffmpeg_src/libavformat/os_support.c',
				'ffmpeg_src/libavformat/paf.c',
				'ffmpeg_src/libavformat/pcm.c',
				'ffmpeg_src/libavformat/pcmdec.c',
				'ffmpeg_src/libavformat/pcmenc.c',
				'ffmpeg_src/libavformat/pjsdec.c',
				'ffmpeg_src/libavformat/pmpdec.c',
				'ffmpeg_src/libavformat/psxstr.c',
				'ffmpeg_src/libavformat/pva.c',
				'ffmpeg_src/libavformat/pvfdec.c',
				'ffmpeg_src/libavformat/qcp.c',
				'ffmpeg_src/libavformat/r3d.c',
				'ffmpeg_src/libavformat/rawdec.c',
				'ffmpeg_src/libavformat/rawenc.c',
				'ffmpeg_src/libavformat/rawvideodec.c',
				'ffmpeg_src/libavformat/realtextdec.c',
				'ffmpeg_src/libavformat/replaygain.c',
				'ffmpeg_src/libavformat/redspark.c',
				'ffmpeg_src/libavformat/riff.c',
				'ffmpeg_src/libavformat/riffdec.c',
				'ffmpeg_src/libavformat/riffenc.c',
				'ffmpeg_src/libavformat/rl2.c',
				'ffmpeg_src/libavformat/rm.c',
				'ffmpeg_src/libavformat/rmdec.c',
				'ffmpeg_src/libavformat/rmenc.c',
				'ffmpeg_src/libavformat/rmsipr.c',
				'ffmpeg_src/libavformat/rpl.c',
				'ffmpeg_src/libavformat/rsd.c',
				'ffmpeg_src/libavformat/rso.c',
				'ffmpeg_src/libavformat/rsodec.c',
				'ffmpeg_src/libavformat/rsoenc.c',
				'ffmpeg_src/libavformat/rdt.c',
				'ffmpeg_src/libavformat/rtp.c',
				'ffmpeg_src/libavformat/rtsp.c',
				'ffmpeg_src/libavformat/rtp.h',
				'ffmpeg_src/libavformat/rtpdec.c',
				'ffmpeg_src/libavformat/rtpdec.h',
				'ffmpeg_src/libavformat/rtpdec_ac3.c',
				'ffmpeg_src/libavformat/rtpdec_amr.c',
				'ffmpeg_src/libavformat/rtpdec_asf.c',
				'ffmpeg_src/libavformat/rtpdec_dv.c',
				'ffmpeg_src/libavformat/rtpdec_formats.h',
				'ffmpeg_src/libavformat/rtpdec_g726.c',
				'ffmpeg_src/libavformat/rtpdec_h261.c',
				'ffmpeg_src/libavformat/rtpdec_h263.c',
				'ffmpeg_src/libavformat/rtpdec_h263_rfc2190.c',
				'ffmpeg_src/libavformat/rtpdec_h264.c',
				'ffmpeg_src/libavformat/rtpdec_hevc.c',
				'ffmpeg_src/libavformat/rtpdec_ilbc.c',
				'ffmpeg_src/libavformat/rtpdec_jpeg.c',
				'ffmpeg_src/libavformat/rtpdec_latm.c',
				'ffmpeg_src/libavformat/rtpdec_mpa_robust.c',
				'ffmpeg_src/libavformat/rtpdec_mpeg12.c',
				'ffmpeg_src/libavformat/rtpdec_mpeg4.c',
				'ffmpeg_src/libavformat/rtpdec_mpegts.c',
				'ffmpeg_src/libavformat/rtpdec_qcelp.c',
				'ffmpeg_src/libavformat/rtpdec_qdm2.c',
				'ffmpeg_src/libavformat/rtpdec_qt.c',
				'ffmpeg_src/libavformat/rtpdec_svq3.c',
				'ffmpeg_src/libavformat/rtpdec_vp8.c',
				'ffmpeg_src/libavformat/rtpdec_vp9.c',
				'ffmpeg_src/libavformat/rtpdec_xiph.c',
				'ffmpeg_src/libavformat/rtpenc.c',
				'ffmpeg_src/libavformat/rtpenc.h',
				'ffmpeg_src/libavformat/rtpenc_aac.c',
				'ffmpeg_src/libavformat/rtpenc_amr.c',
				'ffmpeg_src/libavformat/rtpenc_chain.c',
				'ffmpeg_src/libavformat/rtpenc_chain.h',
				'ffmpeg_src/libavformat/rtpenc_h261.c',
				'ffmpeg_src/libavformat/rtpenc_h263.c',
				'ffmpeg_src/libavformat/rtpenc_h263_rfc2190.c',
				'ffmpeg_src/libavformat/rtpenc_h264_hevc.c',
				'ffmpeg_src/libavformat/rtpenc_jpeg.c',
				'ffmpeg_src/libavformat/rtpenc_latm.c',
				'ffmpeg_src/libavformat/rtpenc_mpegts.c',
				'ffmpeg_src/libavformat/rtpenc_mpv.c',
				'ffmpeg_src/libavformat/rtpenc_vp8.c',
				'ffmpeg_src/libavformat/rtpenc_xiph.c',
				'ffmpeg_src/libavformat/rtpproto.c',
				'ffmpeg_src/libavformat/rtpproto.h',
				'ffmpeg_src/libavformat/srtp.c',
				'ffmpeg_src/libavformat/srtp.h',
				'ffmpeg_src/libavformat/srtpproto.c',
				'ffmpeg_src/libavformat/samidec.c',
				'ffmpeg_src/libavformat/sauce.c',
				'ffmpeg_src/libavformat/sbgdec.c',
				'ffmpeg_src/libavformat/sdp.c',
				'ffmpeg_src/libavformat/sdr2.c',
				#'ffmpeg_src/libavformat/seek.c',
				'ffmpeg_src/libavformat/segafilm.c',
				'ffmpeg_src/libavformat/segment.c',
				'ffmpeg_src/libavformat/sierravmd.c',
				'ffmpeg_src/libavformat/siff.c',
				'ffmpeg_src/libavformat/smacker.c',
				'ffmpeg_src/libavformat/smjpeg.c',
				'ffmpeg_src/libavformat/smjpegdec.c',
				'ffmpeg_src/libavformat/smjpegenc.c',
				'ffmpeg_src/libavformat/smoothstreamingenc.c',
				'ffmpeg_src/libavformat/smush.c',
				'ffmpeg_src/libavformat/sol.c',
				'ffmpeg_src/libavformat/soxdec.c',
				'ffmpeg_src/libavformat/soxenc.c',
				'ffmpeg_src/libavformat/spdif.c',
				'ffmpeg_src/libavformat/spdifdec.c',
				'ffmpeg_src/libavformat/spdifenc.c',
				'ffmpeg_src/libavformat/srtdec.c',
				'ffmpeg_src/libavformat/srtenc.c',
				'ffmpeg_src/libavformat/srtp.c',
				'ffmpeg_src/libavformat/srtpproto.c',
				'ffmpeg_src/libavformat/subfile.c',
				'ffmpeg_src/libavformat/subtitles.c',
				'ffmpeg_src/libavformat/subviewer1dec.c',
				'ffmpeg_src/libavformat/subviewerdec.c',
				'ffmpeg_src/libavformat/swf.c',
				'ffmpeg_src/libavformat/swfdec.c',
				'ffmpeg_src/libavformat/swfenc.c',
				'ffmpeg_src/libavformat/takdec.c',
				'ffmpeg_src/libavformat/tcp.c',
				'ffmpeg_src/libavformat/tedcaptionsdec.c',
				'ffmpeg_src/libavformat/tee.c',
				'ffmpeg_src/libavformat/thp.c',
				'ffmpeg_src/libavformat/tiertexseq.c',
				'ffmpeg_src/libavformat/tmv.c',
				'ffmpeg_src/libavformat/tta.c',
				'ffmpeg_src/libavformat/tty.c',
				'ffmpeg_src/libavformat/txd.c',
				'ffmpeg_src/libavformat/udp.c',
				'ffmpeg_src/libavformat/uncodedframecrcenc.c',
				
				'ffmpeg_src/libavformat/url.c',
				'ffmpeg_src/libavformat/urldecode.c',
				'ffmpeg_src/libavformat/utils.c',
				'ffmpeg_src/libavformat/vivo.c',
				'ffmpeg_src/libavformat/voc.c',
				'ffmpeg_src/libavformat/vocdec.c',
				'ffmpeg_src/libavformat/vocenc.c',
				'ffmpeg_src/libavformat/vorbiscomment.c',
				'ffmpeg_src/libavformat/vplayerdec.c',
				'ffmpeg_src/libavformat/vqf.c',
				'ffmpeg_src/libavformat/w64.c',
				'ffmpeg_src/libavformat/wavdec.c',
				'ffmpeg_src/libavformat/wavenc.c',
				'ffmpeg_src/libavformat/wc3movie.c',
				'ffmpeg_src/libavformat/webvttdec.c',
				'ffmpeg_src/libavformat/webvttenc.c',
				'ffmpeg_src/libavformat/westwood_aud.c',
				'ffmpeg_src/libavformat/westwood_vqa.c',
				'ffmpeg_src/libavformat/wtvdec.c',
				'ffmpeg_src/libavformat/wtvenc.c',
				'ffmpeg_src/libavformat/wtv_common.c',
				'ffmpeg_src/libavformat/wv.c',
				'ffmpeg_src/libavformat/wvdec.c',
				'ffmpeg_src/libavformat/wvenc.c',
				'ffmpeg_src/libavformat/xa.c',
				'ffmpeg_src/libavformat/xmv.c',
				'ffmpeg_src/libavformat/xwma.c',
				'ffmpeg_src/libavformat/yop.c',
				#'ffmpeg_src/libavformat/yuv4mpeg.c'
			],
			'conditions':[
				['OS != "win"',{
					'sources':[
						#'ffmpeg_src/libavformat/unix.c',
					]
				}],
				['OS == "win"',{
					'link_settings': {
						'libraries': [
							'-lws2_32.lib'
						]
					}
				}]
				
			]
		}
		
		
		,{
			'target_name': 'avresample',
			'type':'<(primary_libraries)',
			'dependencies':[
				'avutil',
			],
			'defines':[],
			'include_dirs':[
				'ffmpeg_src',
				'ffmpeg_src/libavresample',
			],
			'direct_dependent_settings': {
				'include_dirs': [
					'ffmpeg_src/libavresample',
				],
			 },
			'sources':[
				'definitions/avresample.def',
				'ffmpeg_src/libavresample/audio_convert.c',
				'ffmpeg_src/libavresample/audio_data.c',
				'ffmpeg_src/libavresample/audio_mix.c',
				'ffmpeg_src/libavresample/audio_mix_matrix.c',
				'ffmpeg_src/libavresample/avresample-test.c',
				'ffmpeg_src/libavresample/dither.c',
				'ffmpeg_src/libavresample/options.c',
				'ffmpeg_src/libavresample/resample.c',
				'ffmpeg_src/libavresample/utils.c'
			],
			'conditions':[
				['target_arch in "ia32 x64"',{
					'includes':[
						'yasm_compile.gypi',
					 ],
					 'variables':{
						'yasm_flags':[
							'-I','ffmpeg_src',
							'-I','config/<(OS)/<(target_arch)',
							'-Pconfig.asm',
							'-DPIC=1',
						 ],
					 },
				}],
			
				['target_arch in "ia32 x64"',{
					'sources':[
						'ffmpeg_src/libavresample/x86/audio_convert.asm',
						'ffmpeg_src/libavresample/x86/audio_convert_init.c',
						'ffmpeg_src/libavresample/x86/audio_mix.asm',
						'ffmpeg_src/libavresample/x86/audio_mix_init.c',
						'ffmpeg_src/libavresample/x86/dither.asm',
						'ffmpeg_src/libavresample/x86/dither_init.c',
						'ffmpeg_src/libavresample/x86/util.asm',
						#'ffmpeg_src/libavresample/x86/w64xmmtest.c',
					],
				}],
				['target_arch == "arm"',{
					'sources':[
						'ffmpeg_src/libavresample/arm/asm-offsets.h',
						'ffmpeg_src/libavresample/arm/audio_convert_init.c',
						'ffmpeg_src/libavresample/arm/audio_convert_neon.S',
						'ffmpeg_src/libavresample/arm/resample_init.c',
						'ffmpeg_src/libavresample/arm/resample_neon.S',				
					],
				}],
			],
		}
		
		
		,{
			'target_name': 'avutil',
			'type':'<(primary_libraries)',
			'dependencies':[
			],
			'defines':[],
			'include_dirs':[
				'ffmpeg_src',
				#'ffmpeg_src/libavutil',
			],
			'direct_dependent_settings': {
				'include_dirs': [
					#'ffmpeg_src/libavutil',
				],
			 },
			 
			 
			'sources':[
				'definitions/avutil.def',
				'ffmpeg_src/libavutil/adler32.c',
				'ffmpeg_src/libavutil/aes.c',
				'ffmpeg_src/libavutil/atomic.c',
				'ffmpeg_src/libavutil/audio_fifo.c',
				'ffmpeg_src/libavutil/avstring.c',
				'ffmpeg_src/libavutil/base64.c',
				'ffmpeg_src/libavutil/blowfish.c',
				'ffmpeg_src/libavutil/bprint.c',
				'ffmpeg_src/libavutil/buffer.c',
				'ffmpeg_src/libavutil/channel_layout.c',
				'ffmpeg_src/libavutil/cpu.c',
				'ffmpeg_src/libavutil/crc.c',
				'ffmpeg_src/libavutil/des.c',
				'ffmpeg_src/libavutil/dict.c',
				'ffmpeg_src/libavutil/downmix_info.c',
				'ffmpeg_src/libavutil/error.c',
				'ffmpeg_src/libavutil/eval.c',
				'ffmpeg_src/libavutil/fifo.c',
				'ffmpeg_src/libavutil/file.c',
				'ffmpeg_src/libavutil/file_open.c',
				'ffmpeg_src/libavutil/float_dsp.c',
				'ffmpeg_src/libavutil/frame.c',
				'ffmpeg_src/libavutil/hash.c',
				'ffmpeg_src/libavutil/hmac.c',
				'ffmpeg_src/libavutil/imgutils.c',
				'ffmpeg_src/libavutil/integer.c',
				#'ffmpeg_src/libavutil/intfloat_readwrite.c',
				'ffmpeg_src/libavutil/intmath.c',
				'ffmpeg_src/libavutil/lfg.c',
				#'ffmpeg_src/libavutil/lls1.c',
				#'ffmpeg_src/libavutil/lls2.c',
				'ffmpeg_src/libavutil/log.c',
				'ffmpeg_src/libavutil/log2_tab.c',
				'ffmpeg_src/libavutil/lzo.c',
				'ffmpeg_src/libavutil/mathematics.c',
				'ffmpeg_src/libavutil/md5.c',
				'ffmpeg_src/libavutil/mem.c',
				'ffmpeg_src/libavutil/murmur3.c',
				'ffmpeg_src/libavutil/opt.c',
				'ffmpeg_src/libavutil/parseutils.c',
				'ffmpeg_src/libavutil/pca.c',
				'ffmpeg_src/libavutil/pixdesc.c',
				'ffmpeg_src/libavutil/random_seed.c',
				'ffmpeg_src/libavutil/rational.c',
				'ffmpeg_src/libavutil/rc4.c',
				'ffmpeg_src/libavutil/ripemd.c',
				'ffmpeg_src/libavutil/samplefmt.c',
				'ffmpeg_src/libavutil/sha.c',
				'ffmpeg_src/libavutil/sha512.c',
				'ffmpeg_src/libavutil/softfloat.c',
				'ffmpeg_src/libavutil/stereo3d.c',
				'ffmpeg_src/libavutil/time.c',
				'ffmpeg_src/libavutil/timecode.c',
				'ffmpeg_src/libavutil/tree.c',
				'ffmpeg_src/libavutil/utf8.c',
				'ffmpeg_src/libavutil/utils.c',
				'ffmpeg_src/libavutil/xga_font_data.c',
				'ffmpeg_src/libavutil/xtea.c',
				'ffmpeg_src/libavutil/pixelutils.c',
				'ffmpeg_src/libavutil/color_utils.c',
				'ffmpeg_src/libavutil/display.c',
				'ffmpeg_src/libavutil/lls.c',
				'ffmpeg_src/compat/strtod.c',
				'ffmpeg_src/libavutil/threadmessage.c',

			],
			'conditions':[
				['target_arch == "arm"',{
					'sources':[					
						'ffmpeg_src/libavutil/arm/asm.S',
						'ffmpeg_src/libavutil/arm/bswap.h',
						'ffmpeg_src/libavutil/arm/cpu.c',
						'ffmpeg_src/libavutil/arm/cpu.h',
						'ffmpeg_src/libavutil/arm/float_dsp_arm.h',
						'ffmpeg_src/libavutil/arm/float_dsp_init_arm.c',
						'ffmpeg_src/libavutil/arm/float_dsp_init_neon.c',
						'ffmpeg_src/libavutil/arm/float_dsp_init_vfp.c',
						'ffmpeg_src/libavutil/arm/float_dsp_neon.S',
						'ffmpeg_src/libavutil/arm/float_dsp_vfp.S',
						'ffmpeg_src/libavutil/arm/intmath.h',
						'ffmpeg_src/libavutil/arm/intreadwrite.h',
						'ffmpeg_src/libavutil/arm/neontest.h',
						'ffmpeg_src/libavutil/arm/timer.h',
					]
				}],
				['target_arch in "ia32 x64"',{
					'includes':[
						'yasm_compile.gypi',
					 ],
					 'variables':{
						'yasm_flags':[
							'-I','ffmpeg_src',
							'-I','config/<(OS)/<(target_arch)',
							'-Pconfig.asm',
							'-DPIC=1',
						 ],
					 },
				}],

				['OS == "win" and MSVS_VERSION == "2013"',{
					 
					 'sources':[
						'compat/msvcrt/snprintf.c'
					 ],
				}],
				['target_arch in "ia32 x64"',{
					'direct_dependent_settings': {
						'include_dirs': [
							'ffmpeg_src/libavutil/x86',
						],
					 },
					'sources':[
						'ffmpeg_src/libavutil/x86/asm.h',
						'ffmpeg_src/libavutil/x86/bswap.h',
						'ffmpeg_src/libavutil/x86/cpu.c',
						'ffmpeg_src/libavutil/x86/cpu.h',
						'ffmpeg_src/libavutil/x86/cpuid.asm',
						'ffmpeg_src/libavutil/x86/emms.asm',
						'ffmpeg_src/libavutil/x86/emms.h',
						'ffmpeg_src/libavutil/x86/float_dsp.asm',
						'ffmpeg_src/libavutil/x86/float_dsp_init.c',
						'ffmpeg_src/libavutil/x86/intreadwrite.h',
						'ffmpeg_src/libavutil/x86/lls.asm',
						'ffmpeg_src/libavutil/x86/lls_init.c',
						'ffmpeg_src/libavutil/x86/timer.h',
						'ffmpeg_src/libavutil/x86/w64xmmtest.h',
						'ffmpeg_src/libavutil/x86/x86inc.asm',
						'ffmpeg_src/libavutil/x86/x86util.asm',
					],
				}],
				[ 'OS in "linux"', {
					'sources':[
					],
					'link_settings': {
						'libraries': [
							'-lpthread',
							'-lrt',
						],
					},
				}],
			]
		}
		
		
		,{
			'target_name': 'postproc',
			'type':'<(primary_libraries)',
			'dependencies':[
				'avutil',
			],
			'defines':[],
			'include_dirs':[
				'ffmpeg_src',
				'ffmpeg_src/libpostproc',
			],
			'direct_dependent_settings': {
				'include_dirs': [
					'ffmpeg_src/libpostproc',
				],
			 },
			'sources':[
				'definitions/postproc.def',
				'ffmpeg_src/libpostproc/postprocess.c'
			]
		}
		
		
		,{
			'target_name': 'swresample',
			'type':'<(primary_libraries)',
			'dependencies':[
				'avutil',
			],
			'defines':[],
			'include_dirs':[
				'ffmpeg_src',
				'ffmpeg_src/libswresample',
			],
			'direct_dependent_settings': {
				'include_dirs': [
					'ffmpeg_src/libswresample',
				],
			 },
			'sources':[
				'definitions/swresample.def',
				'ffmpeg_src/libswresample/audioconvert.c',
				'ffmpeg_src/libswresample/dither.c',
				'ffmpeg_src/libswresample/log2_tab.c',
				#'ffmpeg_src/libswresample/noise_shaping_data.c',
				'ffmpeg_src/libswresample/rematrix.c',
				'ffmpeg_src/libswresample/resample.c',
				'ffmpeg_src/libswresample/swresample.c',
				'ffmpeg_src/libswresample/options.c',
				'ffmpeg_src/libswresample/resample_dsp.c',
			],
			'conditions':[
				['target_arch == "arm"',{
					'sources':[
						'ffmpeg_src/libswresample/arm/audio_convert_init.c',
						'ffmpeg_src/libswresample/arm/audio_convert_neon.S',
						#'ffmpeg_src/libswresample/arm/neontest.c',
					],
				}],
				
				['target_arch in "ia32 x64"',{
					'includes':[
						'yasm_compile.gypi',
					 ],
					 'variables':{
						'yasm_flags':[
							'-I','ffmpeg_src',
							'-I','config/<(OS)/<(target_arch)',
							'-Pconfig.asm',
							'-DPIC=1',
						 ],
					},
				}],
				
				['target_arch in "ia32 x64"',{
					'sources':[
						'ffmpeg_src/libswresample/x86/audio_convert.asm',
						'ffmpeg_src/libswresample/x86/audio_convert_init.c',
						'ffmpeg_src/libswresample/x86/rematrix.asm',
						'ffmpeg_src/libswresample/x86/rematrix_init.c',
						'ffmpeg_src/libswresample/x86/resample.asm',
						'ffmpeg_src/libswresample/x86/resample_init.c',
					],
				}],
			],
		}
		
		,{
			'target_name': 'swscale',
			'type':'<(primary_libraries)',
			'dependencies':[
				'avutil',
				'swscale_p1',
			],
			'include_dirs':[
				'ffmpeg_src',
				'ffmpeg_src/libswscale',
			],
			'direct_dependent_settings': {
				'include_dirs': [
					'ffmpeg_src/libswscale',
				],
			 },
			 
			'sources':[
				'definitions/swscale.def',
				'ffmpeg_src/libswscale/swscale.c',
				'ffmpeg_src/libswscale/utils.c',
				'ffmpeg_src/libswscale/options.c',
				'ffmpeg_src/libswscale/yuv2rgb.c',
			],
		}
		
		,{
			'target_name': 'swscale_p1',
			'type':'<(library)',
			'dependencies':[
				'avutil',
			],
			'defines':[],
			
			'include_dirs':[
				'ffmpeg_src',
				'ffmpeg_src/libswscale',
			],
			'direct_dependent_settings': {
				'include_dirs': [
					'ffmpeg_src/libswscale',
				],
			 },
			 
			'sources':[
				'ffmpeg_src/libswscale/input.c',
				
				'ffmpeg_src/libswscale/output.c',
				'ffmpeg_src/libswscale/rgb2rgb.c',
				'ffmpeg_src/libswscale/swscale_unscaled.c',
				
				
				'ffmpeg_src/libswscale/hscale_fast_bilinear.c',
			],
			'conditions':[
				['OS=="linux"',{
					'cflags':[
						'-fvisibility=hidden',
						'-fPIC',
					],
				}],
				['target_arch in "ia32 x64"',{
					'includes':[
						'yasm_compile.gypi',
					 ],
					 'variables':{
						'yasm_flags':[
							'-I','ffmpeg_src',
							'-I','config/<(OS)/<(target_arch)',
							'-Pconfig.asm',
							'-DPIC=1',
						 ],
					},
				}],

				['target_arch in "ia32 x64"',{
					'sources':[
						'ffmpeg_src/libswscale/x86/input.asm',
						'ffmpeg_src/libswscale/x86/output.asm',
						'ffmpeg_src/libswscale/x86/rgb2rgb.c',
						'ffmpeg_src/libswscale/x86/scale.asm',
						'ffmpeg_src/libswscale/x86/swscale.c',
						#'ffmpeg_src/libswscale/x86/w64xmmtest.c',
						'ffmpeg_src/libswscale/x86/yuv2rgb.c',
						'ffmpeg_src/libswscale/x86/hscale_fast_bilinear_simd.c',
						
					],
				}],
			]
		}
		
		
		
		,{
			'target_name': 'ffmpeg',
			'type':'executable',
			'dependencies':[
				'avcodec',
				'avdevice',
				'swresample',
				'avfilter',
				'avformat',
				'avutil',
				'swscale',
			],
			'defines':[],
			'include_dirs':[
				'ffmpeg_src',
			],
			'direct_dependent_settings': {
				'include_dirs': [
				],
			 },
			'sources':[
				'ffmpeg_src/cmdutils.c',
				'ffmpeg_src/ffmpeg_filter.c',
				'ffmpeg_src/ffmpeg_opt.c',
				'ffmpeg_src/ffmpeg.c',
				

			],
			'msvs_settings': {
				'VCCLCompilerTool': {
			#		'ForcedIncludeFiles' : ['time.h'],
				},
				
			},
			'conditions':[
				 ['OS != "win"', {
					'cflags':[
			#			'-include time.h',
					],
				}]
			]
		}
		
		
	]
}
