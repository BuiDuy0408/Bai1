using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Bai1_QLNhanSu
{
    public partial class Main : Form
    {
        public Main()
        {
            InitializeComponent();
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            label1.Text = label1.Text.Substring(2, label1.Text.Length - 2) + label1.Text.Substring(0, 2);
        }

        private void timer2_Tick(object sender, EventArgs e)
        {
            label1.ForeColor = Color.Yellow;
        }

        private void timer3_Tick(object sender, EventArgs e)
        {
            label1.ForeColor = Color.Red;
        }
    }
}
