// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "Vtop__pch.h"
#include "Vtop___024root.h"

VL_INLINE_OPT void Vtop___024root___ico_sequent__TOP__0(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___ico_sequent__TOP__0\n"); );
    // Body
    vlSelf->fifo__DOT__clk = vlSelf->clk;
    vlSelf->fifo__DOT__rst = vlSelf->rst;
    vlSelf->fifo__DOT__wr_en = vlSelf->wr_en;
    vlSelf->fifo__DOT__din = vlSelf->din;
    vlSelf->fifo__DOT__rd_en = vlSelf->rd_en;
    vlSelf->dout = vlSelf->fifo__DOT__dout;
    vlSelf->full = (8U == (IData)(vlSelf->fifo__DOT__count));
    vlSelf->empty = (0U == (IData)(vlSelf->fifo__DOT__count));
    vlSelf->fifo__DOT__full = vlSelf->full;
    vlSelf->fifo__DOT__do_wr = ((~ (IData)(vlSelf->full)) 
                                & (IData)(vlSelf->wr_en));
    vlSelf->fifo__DOT__empty = vlSelf->empty;
    vlSelf->fifo__DOT__do_rd = ((~ (IData)(vlSelf->empty)) 
                                & (IData)(vlSelf->rd_en));
}

void Vtop___024root___eval_ico(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_ico\n"); );
    // Body
    if ((1ULL & vlSelf->__VicoTriggered.word(0U))) {
        Vtop___024root___ico_sequent__TOP__0(vlSelf);
    }
}

void Vtop___024root___eval_triggers__ico(Vtop___024root* vlSelf);

bool Vtop___024root___eval_phase__ico(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__ico\n"); );
    // Init
    CData/*0:0*/ __VicoExecute;
    // Body
    Vtop___024root___eval_triggers__ico(vlSelf);
    __VicoExecute = vlSelf->__VicoTriggered.any();
    if (__VicoExecute) {
        Vtop___024root___eval_ico(vlSelf);
    }
    return (__VicoExecute);
}

void Vtop___024root___eval_act(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_act\n"); );
}

VL_INLINE_OPT void Vtop___024root___nba_sequent__TOP__0(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___nba_sequent__TOP__0\n"); );
    // Init
    CData/*2:0*/ __Vdly__fifo__DOT__wp;
    __Vdly__fifo__DOT__wp = 0;
    CData/*2:0*/ __Vdlyvdim0__fifo__DOT__mem__v0;
    __Vdlyvdim0__fifo__DOT__mem__v0 = 0;
    CData/*7:0*/ __Vdlyvval__fifo__DOT__mem__v0;
    __Vdlyvval__fifo__DOT__mem__v0 = 0;
    CData/*0:0*/ __Vdlyvset__fifo__DOT__mem__v0;
    __Vdlyvset__fifo__DOT__mem__v0 = 0;
    CData/*2:0*/ __Vdly__fifo__DOT__rp;
    __Vdly__fifo__DOT__rp = 0;
    CData/*3:0*/ __Vdly__fifo__DOT__count;
    __Vdly__fifo__DOT__count = 0;
    // Body
    __Vdly__fifo__DOT__rp = vlSelf->fifo__DOT__rp;
    __Vdly__fifo__DOT__wp = vlSelf->fifo__DOT__wp;
    __Vdlyvset__fifo__DOT__mem__v0 = 0U;
    __Vdly__fifo__DOT__count = vlSelf->fifo__DOT__count;
    if (vlSelf->rst) {
        __Vdly__fifo__DOT__wp = 0U;
        __Vdly__fifo__DOT__count = 0U;
        __Vdly__fifo__DOT__rp = 0U;
        vlSelf->fifo__DOT__dout = 0U;
    } else {
        if (vlSelf->fifo__DOT__do_wr) {
            __Vdlyvval__fifo__DOT__mem__v0 = vlSelf->din;
            __Vdlyvset__fifo__DOT__mem__v0 = 1U;
            __Vdlyvdim0__fifo__DOT__mem__v0 = vlSelf->fifo__DOT__wp;
            __Vdly__fifo__DOT__wp = (7U & ((IData)(1U) 
                                           + (IData)(vlSelf->fifo__DOT__wp)));
        }
        if ((2U == (((IData)(vlSelf->fifo__DOT__do_wr) 
                     << 1U) | (IData)(vlSelf->fifo__DOT__do_rd)))) {
            __Vdly__fifo__DOT__count = (0xfU & ((IData)(1U) 
                                                + (IData)(vlSelf->fifo__DOT__count)));
        } else if ((1U == (((IData)(vlSelf->fifo__DOT__do_wr) 
                            << 1U) | (IData)(vlSelf->fifo__DOT__do_rd)))) {
            __Vdly__fifo__DOT__count = (0xfU & ((IData)(vlSelf->fifo__DOT__count) 
                                                - (IData)(1U)));
        }
        if (vlSelf->fifo__DOT__do_rd) {
            vlSelf->fifo__DOT__dout = vlSelf->fifo__DOT__mem
                [vlSelf->fifo__DOT__rp];
            __Vdly__fifo__DOT__rp = (7U & ((IData)(1U) 
                                           + (IData)(vlSelf->fifo__DOT__rp)));
        }
    }
    vlSelf->fifo__DOT__wp = __Vdly__fifo__DOT__wp;
    vlSelf->fifo__DOT__count = __Vdly__fifo__DOT__count;
    vlSelf->fifo__DOT__rp = __Vdly__fifo__DOT__rp;
    if (__Vdlyvset__fifo__DOT__mem__v0) {
        vlSelf->fifo__DOT__mem[__Vdlyvdim0__fifo__DOT__mem__v0] 
            = __Vdlyvval__fifo__DOT__mem__v0;
    }
    vlSelf->full = (8U == (IData)(vlSelf->fifo__DOT__count));
    vlSelf->empty = (0U == (IData)(vlSelf->fifo__DOT__count));
    vlSelf->dout = vlSelf->fifo__DOT__dout;
    vlSelf->fifo__DOT__full = vlSelf->full;
    vlSelf->fifo__DOT__do_wr = ((~ (IData)(vlSelf->full)) 
                                & (IData)(vlSelf->wr_en));
    vlSelf->fifo__DOT__empty = vlSelf->empty;
    vlSelf->fifo__DOT__do_rd = ((~ (IData)(vlSelf->empty)) 
                                & (IData)(vlSelf->rd_en));
}

void Vtop___024root___eval_nba(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_nba\n"); );
    // Body
    if ((1ULL & vlSelf->__VnbaTriggered.word(0U))) {
        Vtop___024root___nba_sequent__TOP__0(vlSelf);
    }
}

void Vtop___024root___eval_triggers__act(Vtop___024root* vlSelf);

bool Vtop___024root___eval_phase__act(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__act\n"); );
    // Init
    VlTriggerVec<1> __VpreTriggered;
    CData/*0:0*/ __VactExecute;
    // Body
    Vtop___024root___eval_triggers__act(vlSelf);
    __VactExecute = vlSelf->__VactTriggered.any();
    if (__VactExecute) {
        __VpreTriggered.andNot(vlSelf->__VactTriggered, vlSelf->__VnbaTriggered);
        vlSelf->__VnbaTriggered.thisOr(vlSelf->__VactTriggered);
        Vtop___024root___eval_act(vlSelf);
    }
    return (__VactExecute);
}

bool Vtop___024root___eval_phase__nba(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__nba\n"); );
    // Init
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = vlSelf->__VnbaTriggered.any();
    if (__VnbaExecute) {
        Vtop___024root___eval_nba(vlSelf);
        vlSelf->__VnbaTriggered.clear();
    }
    return (__VnbaExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__ico(Vtop___024root* vlSelf);
#endif  // VL_DEBUG
#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__nba(Vtop___024root* vlSelf);
#endif  // VL_DEBUG
#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__act(Vtop___024root* vlSelf);
#endif  // VL_DEBUG

void Vtop___024root___eval(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval\n"); );
    // Init
    IData/*31:0*/ __VicoIterCount;
    CData/*0:0*/ __VicoContinue;
    IData/*31:0*/ __VnbaIterCount;
    CData/*0:0*/ __VnbaContinue;
    // Body
    __VicoIterCount = 0U;
    vlSelf->__VicoFirstIteration = 1U;
    __VicoContinue = 1U;
    while (__VicoContinue) {
        if (VL_UNLIKELY((0x64U < __VicoIterCount))) {
#ifdef VL_DEBUG
            Vtop___024root___dump_triggers__ico(vlSelf);
#endif
            VL_FATAL_MT("/home/jayan_9007/ai-regression-triage/tests/../rtl/fifo.v", 1, "", "Input combinational region did not converge.");
        }
        __VicoIterCount = ((IData)(1U) + __VicoIterCount);
        __VicoContinue = 0U;
        if (Vtop___024root___eval_phase__ico(vlSelf)) {
            __VicoContinue = 1U;
        }
        vlSelf->__VicoFirstIteration = 0U;
    }
    __VnbaIterCount = 0U;
    __VnbaContinue = 1U;
    while (__VnbaContinue) {
        if (VL_UNLIKELY((0x64U < __VnbaIterCount))) {
#ifdef VL_DEBUG
            Vtop___024root___dump_triggers__nba(vlSelf);
#endif
            VL_FATAL_MT("/home/jayan_9007/ai-regression-triage/tests/../rtl/fifo.v", 1, "", "NBA region did not converge.");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        __VnbaContinue = 0U;
        vlSelf->__VactIterCount = 0U;
        vlSelf->__VactContinue = 1U;
        while (vlSelf->__VactContinue) {
            if (VL_UNLIKELY((0x64U < vlSelf->__VactIterCount))) {
#ifdef VL_DEBUG
                Vtop___024root___dump_triggers__act(vlSelf);
#endif
                VL_FATAL_MT("/home/jayan_9007/ai-regression-triage/tests/../rtl/fifo.v", 1, "", "Active region did not converge.");
            }
            vlSelf->__VactIterCount = ((IData)(1U) 
                                       + vlSelf->__VactIterCount);
            vlSelf->__VactContinue = 0U;
            if (Vtop___024root___eval_phase__act(vlSelf)) {
                vlSelf->__VactContinue = 1U;
            }
        }
        if (Vtop___024root___eval_phase__nba(vlSelf)) {
            __VnbaContinue = 1U;
        }
    }
}

#ifdef VL_DEBUG
void Vtop___024root___eval_debug_assertions(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_debug_assertions\n"); );
    // Body
    if (VL_UNLIKELY((vlSelf->clk & 0xfeU))) {
        Verilated::overWidthError("clk");}
    if (VL_UNLIKELY((vlSelf->rst & 0xfeU))) {
        Verilated::overWidthError("rst");}
    if (VL_UNLIKELY((vlSelf->wr_en & 0xfeU))) {
        Verilated::overWidthError("wr_en");}
    if (VL_UNLIKELY((vlSelf->rd_en & 0xfeU))) {
        Verilated::overWidthError("rd_en");}
}
#endif  // VL_DEBUG
