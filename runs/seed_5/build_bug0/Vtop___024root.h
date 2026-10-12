// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vtop.h for the primary calling header

#ifndef VERILATED_VTOP___024ROOT_H_
#define VERILATED_VTOP___024ROOT_H_  // guard

#include "verilated.h"


class Vtop__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vtop___024root final : public VerilatedModule {
  public:

    // DESIGN SPECIFIC STATE
    VL_IN8(clk,0,0);
    VL_IN8(rst,0,0);
    VL_IN8(wr_en,0,0);
    VL_IN8(din,7,0);
    VL_IN8(rd_en,0,0);
    VL_OUT8(dout,7,0);
    VL_OUT8(full,0,0);
    VL_OUT8(empty,0,0);
    CData/*0:0*/ fifo__DOT__clk;
    CData/*0:0*/ fifo__DOT__rst;
    CData/*0:0*/ fifo__DOT__wr_en;
    CData/*7:0*/ fifo__DOT__din;
    CData/*0:0*/ fifo__DOT__rd_en;
    CData/*7:0*/ fifo__DOT__dout;
    CData/*0:0*/ fifo__DOT__full;
    CData/*0:0*/ fifo__DOT__empty;
    CData/*3:0*/ fifo__DOT__count;
    CData/*2:0*/ fifo__DOT__wp;
    CData/*2:0*/ fifo__DOT__rp;
    CData/*0:0*/ fifo__DOT__do_wr;
    CData/*0:0*/ fifo__DOT__do_rd;
    CData/*0:0*/ __VstlFirstIteration;
    CData/*0:0*/ __VicoFirstIteration;
    CData/*0:0*/ __Vtrigprevexpr___TOP__clk__0;
    CData/*0:0*/ __VactContinue;
    IData/*31:0*/ __VactIterCount;
    VlUnpacked<CData/*7:0*/, 8> fifo__DOT__mem;
    VlTriggerVec<1> __VstlTriggered;
    VlTriggerVec<1> __VicoTriggered;
    VlTriggerVec<1> __VactTriggered;
    VlTriggerVec<1> __VnbaTriggered;

    // INTERNAL VARIABLES
    Vtop__Syms* const vlSymsp;

    // PARAMETERS
    static constexpr IData/*31:0*/ fifo__DOT__W = 8U;
    static constexpr IData/*31:0*/ fifo__DOT__D = 8U;

    // CONSTRUCTORS
    Vtop___024root(Vtop__Syms* symsp, const char* v__name);
    ~Vtop___024root();
    VL_UNCOPYABLE(Vtop___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
