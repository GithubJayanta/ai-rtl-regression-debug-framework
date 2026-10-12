module fifo #(parameter W=8, D=8)(
  input clk, input rst, input wr_en, input [W-1:0] din,
  input rd_en, output reg [W-1:0] dout, output full, output empty);
  reg [W-1:0] mem [0:D-1];
  reg [$clog2(D):0] count;
  reg [$clog2(D)-1:0] wp, rp;
  assign full  = (count == D);
  assign empty = (count == 0);
`ifdef BUG
  wire do_wr = wr_en;            // bug: ignores full
`else
  wire do_wr = wr_en && !full;
`endif
  wire do_rd = rd_en && !empty;
  always @(posedge clk) begin
    if (rst) begin wp<=0; rp<=0; count<=0; dout<=0; end
    else begin
      if (do_wr) begin mem[wp] <= din; wp <= wp+1; end
      if (do_rd) begin dout <= mem[rp]; rp <= rp+1; end
      case ({do_wr, do_rd})
        2'b10: count <= count+1;
        2'b01: count <= count-1;
        default: ;
      endcase
    end
  end
endmodule
