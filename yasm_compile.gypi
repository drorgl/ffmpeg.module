# Copyright (c) 2012 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# This is an gyp include to use YASM for compiling assembly files.
#
# Files to be compiled with YASM should have an extension of .asm.
#
# There are two variables for this include:
# yasm_flags : Pass additional flags into YASM.
# yasm_output_path : Output directory for the compiled object files.
#
# Sample usage:
# 'sources': [
#   'ultra_optimized_awesome.asm',
# ],
# 'variables': {
#   'yasm_flags': [
#     '-I', 'assembly_include',
#   ],
#   'yasm_output_path': '<(SHARED_INTERMEDIATE_DIR)/project',
# },
# 'includes': [
#   'third_party/yasm/yasm_compile.gypi'
# ],

{
  'variables': {
    'yasm_flags': [],

    'conditions': [
      [ 'use_system_yasm==0', {
        'yasm_path': 'vsyasm<(EXECUTABLE_SUFFIX)',
      }, {
        'yasm_path': '<!(which yasm)',
      }],

      # Define yasm_flags that pass into YASM.
      
	  ['target_arch=="ia32"',{
		'yasm_flags': [
		  '-DARCH_X86_64=0',
		  '-DARCH_X86_32=1',
		  '--machine=x86',
		],
	  }],
	  
	  ['target_arch=="x64"',{
		'yasm_flags': [
		  '-DARCH_X86_32=0',
		  '-DARCH_X86_64=1',
		  '--machine=amd64',
		],
	  }],
	  
	  [ 'OS=="linux" and target_arch=="ia32"', {
        'yasm_flags': [
          '--oformat=elf32',
        ],
      }],
	  [ 'OS=="linux" and target_arch=="x64"', {
        'yasm_flags': [
          '--oformat=elf64',
        ],
      }],
	  
      [ 'OS=="win" and target_arch=="ia32"', {
        'yasm_flags': [
		  '-Xvc',
		  '-s',
		  '-DPREFIX',
          '--oformat=win32',
        ],
      }],
	  [ 'OS=="win" and target_arch=="x64"', {
        'yasm_flags': [
		  '-Xvc',
		  '-s',
		  '-DPREFIX',
          '--oformat=win64',
        ],
      }],

      # Define output extension.
      ['OS=="win"', {
        'asm_obj_extension': 'obj',
      }, {
        'asm_obj_extension': 'o',
      }],
    ],
  },  # variables

  'conditions': [
    # Only depend on YASM on x86 systems, do this so that compiling
    # .asm files for ARM will fail.
    ['use_system_yasm==0 and ( target_arch=="ia32" or target_arch=="x64" )', {
      #'dependencies': [
      #  '<(DEPTH)/yasm.gyp:yasm#host',
      #],
    }],
  ],  # conditions

  'rules': [
    {
      'rule_name': 'assemble',
      'extension': 'asm',
      'inputs': [],
      'outputs': [
        '<(yasm_output_path)/<(RULE_INPUT_ROOT).<(asm_obj_extension)',
      ],
      'action': [
        '<(yasm_path)',
        '<@(yasm_flags)',
        '-o', '<(yasm_output_path)/<(RULE_INPUT_ROOT).<(asm_obj_extension)',
        '<(RULE_INPUT_PATH)',
      ],
	  'msvs_cygwin_shell': 0,
      'process_outputs_as_sources': 1,
      'message': 'Compile assembly <(RULE_INPUT_PATH).',
    },
  ],  # rules
}