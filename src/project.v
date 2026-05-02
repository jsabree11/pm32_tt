`default_nettype none

module tt_um_pm32 (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    reg [31:0] mc;
    reg [31:0] mp;

    wire [63:0] p;
    wire done;

    wire rst = ~rst_n;

    // Controls from uio_in
    wire load_mc = uio_in[0];
    wire load_mp = uio_in[1];
    wire start_button = uio_in[2];
    wire [1:0] byte_sel = uio_in[4:3];
    wire [2:0] out_sel  = uio_in[7:5];

    reg start_d;
    always @(posedge clk or posedge rst) begin
        if (rst)
            start_d <= 1'b0;
        else
            start_d <= start_button;
    end

    wire start_pulse = start_button & ~start_d;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            mc <= 32'b0;
            mp <= 32'b0;
        end else begin
            if (load_mc) begin
                case (byte_sel)
                    2'd0: mc[7:0]   <= ui_in;
                    2'd1: mc[15:8]  <= ui_in;
                    2'd2: mc[23:16] <= ui_in;
                    2'd3: mc[31:24] <= ui_in;
                endcase
            end

            if (load_mp) begin
                case (byte_sel)
                    2'd0: mp[7:0]   <= ui_in;
                    2'd1: mp[15:8]  <= ui_in;
                    2'd2: mp[23:16] <= ui_in;
                    2'd3: mp[31:24] <= ui_in;
                endcase
            end
        end
    end

    pm32 mult (
        .clk(clk),
        .rst(rst),
        .start(start_pulse),
        .mc(mc),
        .mp(mp),
        .p(p),
        .done(done)
    );

    assign uo_out = p[out_sel*8 +: 8];

    assign uio_out = {7'b0, done};
    assign uio_oe  = 8'b00000001;

    wire _unused = &{ena, 1'b0};

endmodule
