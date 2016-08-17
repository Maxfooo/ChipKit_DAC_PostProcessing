


module Operating_DAC_Top
(
	trigger,
	pbReset,
	pinReset,
	clk,
	leds,
	dacVal
);

parameter PRECISION = 12;

input trigger;
input pbReset;
wire pbrst;
input pinReset;
wire pinrst;
input clk;

output [7:0] leds;
output [PRECISION-1:0] dacVal;

assign leds = dacVal[7:0];

pushbtnReset pbr_0(
	.clk(clk),
	.rstIn(pbReset),
	.rstOut(pbrst)
);

pushbtnReset pbr_1(
	.clk(clk),
	.rstIn(pinReset),
	.rstOut(pinrst)
);

wire reset;
assign reset = pbrst | pinrst;

Operating_DAC op_DAC_0
(
	.trigger(trigger),
	.reset(reset),
	.dacVal(dacVal)
);

endmodule
