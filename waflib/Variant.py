#!/usr/bin/env python
# encoding: utf-8
# Roland Puntaier, 2017

"""If there is a *variants* variable in the main wscript

- x_variant commandline arguments are created
  for x in {configure, build, clean, install, uninstall}
- an x command line argument is expanded to all x_variant's 
- the associated x function context contains :py:const:`variant`

Variant strings can use the `/` path separator to produce an according output tree.

"""

from waflib.Build import BuildContext, CleanContext, InstallContext, UninstallContext
from waflib.Configure import ConfigurationContext
from waflib import Context
from waflib import Options

class VariantContext(Context.Context):
	"wscript global variants implicitly expanded to configure_x, build_x,..."
	cmd = 'init'
	fun = 'init'
	def execute(self):
		try:
			Context.Context.execute(self)
			vs = list(Context.g_module.variants)
			cls = [cl for cl in Context.classes if issubclass(cl,BuildContext)]
			for y in [ConfigurationContext]+cls:
				c = y.__name__.replace('Context','').replace('ation','e').lower()
				cvs = []
				for v in vs:
					cv = self.add_variant(y,c,v)
					cvs.append(cv)
				cmds = []
				for k in Options.commands:
					if k == c:
						cmds.extend(cvs)
					else:
						cmds.append(k)
				Options.commands[:] = cmds
		except AttributeError:
			pass
	def add_variant(self,y,c,v):
		cv = c + '_' + v
		class _variant_context(y):
			cmd = cv
			fun = c
			variant = v
			def __init__(s, **kw):
				y.__init__(s, **kw)
				if c[-1]=='e':#configure
					s.setenv(v)
		return cv
