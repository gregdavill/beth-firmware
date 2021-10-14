#
# This file is part of LiteX.
#
# Copyright (c) 2021 Franck Jullien <franck.jullien@collshade.fr>
# SPDX-License-Identifier: BSD-2-Clause

# FIXME: Cleanup/Move.

import os

from migen import *
from migen.genlib.cdc import *
from migen import ClockDomain

from litex.build.generic_platform import *
from litex.soc.interconnect import axi

from litex.build import tools

# Efinix DDR ---------------------------------------------------------------------------------------

class EfinixDDR(Module):
    def __init__(self, platform, config, cd):
        self.blocks   = []
        self.platform = platform
        self.config   = config
        self.nb_ports = 1

        if config["ports"] != None:
            self.nb_ports = self.config["ports"]

        # TODO: set clock_domain ?
        self.port0 = port0 = axi.AXIInterface(data_width=256, address_width=32, id_width=8)

        if self.nb_ports == 2:
            self.port1 = port1 = axi.AXIInterface(data_width=256, address_width=32, id_width=8)

        for i in range(self.nb_ports):
            ios = [('axi', i,
                Subsignal('wdata',   Pins(256)),
                Subsignal('wready',  Pins(1)),
                Subsignal('wid',     Pins(8)),
                Subsignal('bready',  Pins(1)),
                Subsignal('rdata',   Pins(256)),
                Subsignal('aid',     Pins(8)),
                Subsignal('bvalid',  Pins(1)),
                Subsignal('rlast',   Pins(1)),
                Subsignal('bid',     Pins(8)),
                Subsignal('asize',   Pins(3)),
                Subsignal('atype',   Pins(1)),
                Subsignal('aburst',  Pins(2)),
                Subsignal('wvalid',  Pins(1)),
                Subsignal('aaddr',   Pins(32)),
                Subsignal('rid',     Pins(8)),
                Subsignal('avalid',  Pins(1)),
                Subsignal('rvalid',  Pins(1)),
                Subsignal('alock',   Pins(2)),
                Subsignal('rready',  Pins(1)),
                Subsignal('rresp',   Pins(2)),
                Subsignal('wstrb',   Pins(32)),
                Subsignal('aready',  Pins(1)),
                Subsignal('alen',    Pins(8)),
                Subsignal('wlast',   Pins(1)),
            )]

            io = platform.add_iface_ios(ios)

            port = port0
            if i == 1:
                port = port1

            is_read = port.ar.valid
            self.comb += [
                io.aaddr.eq(Mux(is_read,     port.ar.addr,      port.aw.addr)),
                io.aid.eq(Mux(is_read,         port.ar.id,        port.aw.id)),
                io.alen.eq(Mux(is_read,        port.ar.len,       port.aw.len)),
                io.asize.eq(Mux(is_read,       port.ar.size[0:4], port.aw.size[0:4])), #TODO: check
                io.aburst.eq(Mux(is_read,      port.ar.burst,     port.aw.burst)),
                io.alock.eq(Mux(is_read,       port.ar.lock,      port.aw.lock)),
                io.avalid.eq(Mux(is_read,      port.ar.valid,     port.aw.valid)),

                io.atype.eq(~is_read),
                port.aw.ready.eq(io.aready),
                port.ar.ready.eq(io.aready),

                io.wid.eq(port.w.id),
                io.wstrb.eq(port.w.strb),
                io.wdata.eq(port.w.data),
                io.wlast.eq(port.w.last),
                io.wvalid.eq(port.w.valid),
                port.w.ready.eq(io.wready),

                port.r.id.eq(io.rid),
                port.r.data.eq(io.rdata),
                port.r.last.eq(io.rlast),
                port.r.resp.eq(io.rresp),
                port.r.valid.eq(io.rvalid),
                io.rready.eq(port.r.ready),

                port.b.id.eq(io.bid),
                port.b.valid.eq(io.bvalid),
                io.bready.eq(port.b.ready),
                # port.b.resp ??
            ]
