# Copyright 2013, Qualcomm Innovation Center, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
import SCons.Builder
import os

def _jsdoc2_emitter(target, source, env):
    if len(target) > 1:
        print('scons: *** Only one target may be specified for the jsdoc2 Builder.')
        exit(1)
    if type(target[0]) != SCons.Node.FS.Dir:
        print('scons: *** Target MUST be a Dir node.')
        exit(1);
    # walk the JSDOC_TEMPLATE dir and add the files in the demplate dir to the
    # source list.  This way documentation will be rebuilt if a template file is
    # modified
    template_dir = env.Dir('$JSDOC_TEMPLATE')
    for root, dir, filenames in os.walk(str(template_dir)):
        for f in filenames:
            source.append(root + os.sep + f)
    # make sure the output directory is cleaned.
    env.Clean(source, target[0])
    return target, source

_jsdoc2_builder = SCons.Builder.Builder(
    action ='java -jar ${JSDOC_JSRUN} ${JSDOC_RUN} ${JSDOC_FLAGS} -t=${JSDOC_TEMPLATE} -d=${TARGET} ${SOURCES}',
    src_suffix = '$JSDOC_SUFFIX',
    emitter = _jsdoc2_emitter
)

def generate(env):
    env.Append(BUILDERS = {
        'jsdoc2': _jsdoc2_builder,
    })

    env.AppendUnique(
        # Suffixes/prefixes
        JSDOC_SUFFIX = '.js',
        # JSDoc 2 build flags
        JSDOC_FLAGS = '',
        # full path qualified location of jsrun.jar from JSDoc 2
        JSDOC_JSRUN = 'jsrun.jar',
        # full path qualified location of run.js from JSDoc 2
        JSDOC_RUN = 'run.js',
        # directory containing the publish.js and other template files.
        JSDOC_TEMPLATE = env.Dir('templates')
    )

def exists(env):
    """
    Make sure jsDoc exists.
    """
    java_exists = env.Detect('java')
    jsrun_exists = env.Detect('$JSDOC_JSRUN')
    run_exists = env.Detect('$JSDOC_RUN')
    return (java_exists and jsrun_exists and run_exists)
