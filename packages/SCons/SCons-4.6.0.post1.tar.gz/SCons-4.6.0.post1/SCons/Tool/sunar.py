"""SCons.Tool.sunar

Tool-specific initialization for Solaris (Forte) ar (library archive). If CC
exists, static libraries should be built with it, so that template
instantiations can be resolved.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.
"""

#
# __COPYRIGHT__
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

import SCons.Defaults
import SCons.Tool
import SCons.Util

def generate(env) -> None:
    """Add Builders and construction variables for ar to an Environment."""
    SCons.Tool.createStaticLibBuilder(env)
    
    if env.Detect('CC'):
        env['AR']          = 'CC'
        env['ARFLAGS']     = SCons.Util.CLVar('-xar')
        env['ARCOM']       = '$AR $ARFLAGS -o $TARGET $SOURCES'
    else:
        env['AR']          = 'ar'
        env['ARFLAGS']     = SCons.Util.CLVar('r')
        env['ARCOM']       = '$AR $ARFLAGS $TARGET $SOURCES'

    env['LIBPREFIX']   = 'lib'
    env['LIBSUFFIX']   = '.a'

def exists(env):
    return env.Detect('CC') or env.Detect('ar')

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
