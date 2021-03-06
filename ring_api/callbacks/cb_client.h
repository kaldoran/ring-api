/*
 *  Copyright (C) 2016 Savoir-faire Linux Inc.
 *
 *  Author: Seva Ivanov <seva.ivanov@savoirfairelinux.com>
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA.
 */

#ifndef CB_CLIENT_H
#define CB_CLIENT_H

#include <functional>

#include <dring.h>
#include <configurationmanager_interface.h>

#include "logger.h" // is extra for devs

#include <Python.h>
#include "dring_cython.h" // has generated C callbacks

class CallbacksClient {
    public:
        CallbacksClient();
        ~CallbacksClient();

        void registerEvents();
};
#endif
