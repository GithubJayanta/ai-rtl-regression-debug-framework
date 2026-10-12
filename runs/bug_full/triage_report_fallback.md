LLM unavailable (503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}). Raw failures:
[
  {
    "seed": 1,
    "errors": [
      "full mismatch cycle=24, actual=0, expected=1, occupancy=8, wr=1, rd=0"
    ],
    "first_fail_cycle": 24,
    "fail_sim_time_ns": 281.0,
    "waveform_evidence": {
      "timescale_ns_per_unit": 0.001,
      "failure_time_ns": 281.0,
      "signals": [
        "fifo.clk",
        "fifo.count",
        "fifo.do_rd",
        "fifo.do_wr",
        "fifo.empty",
        "fifo.full",
        "fifo.rd_en",
        "fifo.rp",
        "fifo.rst",
        "fifo.wp",
        "fifo.wr_en"
      ],
      "transitions": [
        {
          "time_ns": 235.0,
          "signal": "fifo.clk",
          "value": "0"
        },
        {
          "time_ns": 235.0,
          "signal": "fifo.rd_en",
          "value": "1"
        },
        {
          "time_ns": 235.0,
          "signal": "fifo.do_rd",
          "value": "1"
        },
        {
          "time_ns": 240.0,
          "signal": "fifo.clk",
          "value": "1"
        },
        {
          "time_ns": 240.0,
          "signal": "fifo.wp",
          "value": "110"
        },
        {
          "time_ns": 240.0,
          "signal": "fifo.rp",
          "value": "000"
        },
        {
          "time_ns": 245.0,
          "signal": "fifo.clk",
          "value": "0"
        },
        {
          "time_ns": 245.0,
          "signal": "fifo.rd_en",
          "value": "0"
        },
        {
          "time_ns": 245.0,
          "signal": "fifo.do_rd",
          "value": "0"
        },
        {
          "time_ns": 250.0,
          "signal": "fifo.clk",
          "value": "1"
        },
        {
          "time_ns": 250.0,
          "signal": "fifo.count",
          "value": "0111"
        },
        {
          "time_ns": 250.0,
          "signal": "fifo.wp",
          "value": "111"
        },
        {
          "time_ns": 255.0,
          "signal": "fifo.clk",
          "value": "0"
        },
        {
          "time_ns": 255.0,
          "signal": "fifo.wr_en",
          "value": "0"
        },
        {
          "time_ns": 255.0,
          "signal": "fifo.do_wr",
          "value": "0"
        },
        {
          "time_ns": 260.0,
          "signal": "fifo.clk",
          "value": "1"
        },
        {
          "time_ns": 265.0,
          "signal": "fifo.clk",
          "value": "0"
        },
        {
          "time_ns": 265.0,
          "signal": "fifo.wr_en",
          "value": "1"
        },
        {
          "time_ns": 265.0,
          "signal": "fifo.do_wr",
          "value": "1"
        },
        {
          "time_ns": 270.0,
          "signal": "fifo.clk",
          "value": "1"
        },
        {
          "time_ns": 270.0,
          "signal": "fifo.full",
          "value": "1"
        },
        {
          "time_ns": 270.0,
          "signal": "fifo.count",
          "value": "1000"
        },
        {
          "time_ns": 270.0,
          "signal": "fifo.wp",
          "value": "000"
        },
        {
          "time_ns": 275.0,
          "signal": "fifo.clk",
          "value": "0"
        },
        {
          "time_ns": 280.0,
          "signal": "fifo.clk",
          "value": "1"
        },
        {
          "time_ns": 280.0,
          "signal": "fifo.full",
          "value": "0"
        },
        {
          "time_ns": 280.0,
          "signal": "fifo.count",
          "value": "1001"
        },
        {
          "time_ns": 280.0,
          "signal": "fifo.wp",
          "value": "001"
        }
      ]
    }
  },
  {
    "seed": 2,
    "errors": [
      "full mismatch cycle=63, actual=0, expected=1, occupancy=8, wr=1, rd=0"
    ],
    "first_fail_cycle": 63,
    "fail_sim_time_ns": 671.0,
    "waveform_evidence": {
      "timescale_ns_per_unit": 0.001,
      "failure_time_ns": 671.0,
      "signals": [
        "fifo.clk",
        "fifo.count",
        "fifo.do_rd",
        "fifo.do_wr",
        "fifo.empty",
        "fifo.full",
        "fifo.rd_en",
        "fifo.rp",
        "fifo.rst",
        "fifo.wp",
        "fifo.wr_en"
      ],
      "transitions": [
        {
          "time_ns": 625.0,
          "signal": "fifo.clk",
          "value": "0"
        },
        {
          "time_ns": 625.0,
          "signal": "fifo.rd_en",
          "value": "0"
        },
        {
          "time_ns": 625.0,
          "signal": "fifo.do_rd",
          "value": "0"
        },
        {
          "time_ns": 630.0,
          "signal": "fifo.clk",
          "value": "1"
        },
        {
          "time_ns": 630.0,
          "signal": "fifo.count",
          "value": "0111"
        },
        {
          "time_ns": 630.0,
          "signal": "fifo.wp",
          "value": "001"
        },
        {
          "time_ns": 635.0,
          "signal": "fifo.clk",
          "value": "0"
        },
        {
          "time_ns": 635.0,
          "signal": "fifo.rd_en",
          "value": "1"
        },
        {
          "time_ns": 635.0,
          "signal": "fifo.do_rd",
          "value": "1"
        },
        {
          "time_ns": 640.0,
          "signal": "fifo.clk",
          "value": "1"
        },
        {
          "time_ns": 640.0,
          "signal": "fifo.wp",
          "value": "010"
        },
        {
          "time_ns": 640.0,
          "signal": "fifo.rp",
          "value": "011"
        },
        {
          "time_ns": 645.0,
          "signal": "fifo.clk",
          "value": "0"
        },
        {
          "time_ns": 650.0,
          "signal": "fifo.clk",
          "value": "1"
        },
        {
          "time_ns": 650.0,
          "signal": "fifo.wp",
          "value": "011"
        },
        {
          "time_ns": 650.0,
          "signal": "fifo.rp",
          "value": "100"
        },
        {
          "time_ns": 655.0,
          "signal": "fifo.clk",
          "value": "0"
        },
        {
          "time_ns": 655.0,
          "signal": "fifo.rd_en",
          "value": "0"
        },
        {
          "time_ns": 655.0,
          "signal": "fifo.do_rd",
          "value": "0"
        },
        {
          "time_ns": 660.0,
          "signal": "fifo.clk",
          "value": "1"
        },
        {
          "time_ns": 660.0,
          "signal": "fifo.full",
          "value": "1"
        },
        {
          "time_ns": 660.0,
          "signal": "fifo.count",
          "value": "1000"
        },
        {
          "time_ns": 660.0,
          "signal": "fifo.wp",
          "value": "100"
        },
        {
          "time_ns": 665.0,
          "signal": "fifo.clk",
          "value": "0"
        },
        {
          "time_ns": 670.0,
          "signal": "fifo.clk",
          "value": "1"
        },
        {
          "time_ns": 670.0,
          "signal": "fifo.full",
          "value": "0"
        },
        {
          "time_ns": 670.0,
          "signal": "fifo.count",
          "value": "1001"
        },
        {
          "time_ns": 670.0,
          "signal": "fifo.wp",
          "value": "101"
        }
      ]
    }
  }
]
