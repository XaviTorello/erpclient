# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import ConfigParser
import os
import logging
from options import configmanager, get_home_dir


class ServersConfig(configmanager):
    """
    Class to load servers definitions from a configfile:
    - passed file name
    - env OPENERPRCSERVERS
    - ~/.openerprc.servers
    """
    def __init__(self, fname=None):
        self.__prefix = None
        self.options = {}
        self.rcfile = self._get_rcfile(fname)
        self.load()

    def load(self, fname=None):
        """
        Load a config file as a dict
        {
            [key]: {
                [opt1]: value,
                [op2]: value2,
            },
            [key2]: {
                [opt1]: value,
            },
            ...
        """
        try:
            self.rcexist = False
            if not os.path.isfile(self.rcfile):
                self.save()
                return False
            self.rcexist = True

            p = ConfigParser.RawConfigParser()
            p.read([self.rcfile])

            for section in p.sections():
                if section not in self.options:
                    self.options[section] = {}

                for (name,value) in p.items(section):
                    if value=='True' or value=='true':
                        value = True
                    if value=='False' or value=='false':
                        value = False
                    if value=='None' or value=='none':
                        value = None
                    self.options[section][name] = value

        except Exception, e:
            import logging
            log = logging.getLogger('common.options')
            log.warn('Unable to read server config file %s !'% (self.rcfile,))
        return True

    def save(self, fname = None):
        """
        Override save method to not alter server file
        """
        return True

    def _get_rcfile(self, fname):
        """
        Override the way that the file is located

        - If passed, use the fname
        - Try to fetch env var OPENERPRCSERVERS
        - Try to locate a .openerprc.servers file at user home
        """
        rcfile = fname or os.environ.get('OPENERPRCSERVERS') or os.path.join(get_home_dir(), '.openerprc.servers')
        if not os.path.exists(rcfile):
            log = logging.getLogger('common.options')
            additional_info = ""
            if optconfigfile:
                additional_info = " Be sure to specify an absolute path name if you are using the '-c' command line switch"
            log.warn('Config file %s does not exist !%s'% (rcfile, additional_info ))
        return os.path.abspath(rcfile)


servers_config = ServersConfig()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
