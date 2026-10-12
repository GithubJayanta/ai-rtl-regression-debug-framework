// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Tracing implementation internals
#include "verilated_vcd_c.h"
#include "Vtop__Syms.h"


void Vtop___024root__trace_chg_0_sub_0(Vtop___024root* vlSelf, VerilatedVcd::Buffer* bufp);

void Vtop___024root__trace_chg_0(void* voidSelf, VerilatedVcd::Buffer* bufp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root__trace_chg_0\n"); );
    // Init
    Vtop___024root* const __restrict vlSelf VL_ATTR_UNUSED = static_cast<Vtop___024root*>(voidSelf);
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    if (VL_UNLIKELY(!vlSymsp->__Vm_activity)) return;
    // Body
    Vtop___024root__trace_chg_0_sub_0((&vlSymsp->TOP), bufp);
}

void Vtop___024root__trace_chg_0_sub_0(Vtop___024root* vlSelf, VerilatedVcd::Buffer* bufp) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root__trace_chg_0_sub_0\n"); );
    // Init
    uint32_t* const oldp VL_ATTR_UNUSED = bufp->oldp(vlSymsp->__Vm_baseCode + 1);
    // Body
    bufp->chgBit(oldp+0,(vlSelf->clk));
    bufp->chgBit(oldp+1,(vlSelf->rst));
    bufp->chgBit(oldp+2,(vlSelf->wr_en));
    bufp->chgCData(oldp+3,(vlSelf->din),8);
    bufp->chgBit(oldp+4,(vlSelf->rd_en));
    bufp->chgCData(oldp+5,(vlSelf->dout),8);
    bufp->chgBit(oldp+6,(vlSelf->full));
    bufp->chgBit(oldp+7,(vlSelf->empty));
    bufp->chgBit(oldp+8,(vlSelf->fifo__DOT__clk));
    bufp->chgBit(oldp+9,(vlSelf->fifo__DOT__rst));
    bufp->chgBit(oldp+10,(vlSelf->fifo__DOT__wr_en));
    bufp->chgCData(oldp+11,(vlSelf->fifo__DOT__din),8);
    bufp->chgBit(oldp+12,(vlSelf->fifo__DOT__rd_en));
    bufp->chgCData(oldp+13,(vlSelf->fifo__DOT__dout),8);
    bufp->chgBit(oldp+14,(vlSelf->fifo__DOT__full));
    bufp->chgBit(oldp+15,(vlSelf->fifo__DOT__empty));
    bufp->chgCData(oldp+16,(vlSelf->fifo__DOT__mem[0]),8);
    bufp->chgCData(oldp+17,(vlSelf->fifo__DOT__mem[1]),8);
    bufp->chgCData(oldp+18,(vlSelf->fifo__DOT__mem[2]),8);
    bufp->chgCData(oldp+19,(vlSelf->fifo__DOT__mem[3]),8);
    bufp->chgCData(oldp+20,(vlSelf->fifo__DOT__mem[4]),8);
    bufp->chgCData(oldp+21,(vlSelf->fifo__DOT__mem[5]),8);
    bufp->chgCData(oldp+22,(vlSelf->fifo__DOT__mem[6]),8);
    bufp->chgCData(oldp+23,(vlSelf->fifo__DOT__mem[7]),8);
    bufp->chgCData(oldp+24,(vlSelf->fifo__DOT__count),4);
    bufp->chgCData(oldp+25,(vlSelf->fifo__DOT__wp),3);
    bufp->chgCData(oldp+26,(vlSelf->fifo__DOT__rp),3);
    bufp->chgBit(oldp+27,(vlSelf->fifo__DOT__do_wr));
    bufp->chgBit(oldp+28,(vlSelf->fifo__DOT__do_rd));
}

void Vtop___024root__trace_cleanup(void* voidSelf, VerilatedVcd* /*unused*/) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root__trace_cleanup\n"); );
    // Init
    Vtop___024root* const __restrict vlSelf VL_ATTR_UNUSED = static_cast<Vtop___024root*>(voidSelf);
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VlUnpacked<CData/*0:0*/, 1> __Vm_traceActivity;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        __Vm_traceActivity[__Vi0] = 0;
    }
    // Body
    vlSymsp->__Vm_activity = false;
    __Vm_traceActivity[0U] = 0U;
}
