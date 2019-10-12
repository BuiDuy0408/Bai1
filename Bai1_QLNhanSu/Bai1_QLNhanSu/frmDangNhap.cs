using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using BangQLCT;
namespace Bai1_QLNhanSu
{
    public partial class frmDangNhap : Form
    {
        public frmDangNhap()
        {
            InitializeComponent();
        }

        BUS_DangNhap dn = new BUS_DangNhap();

        private void btnDangNhap_Click(object sender, EventArgs e)
        {
            if (dn.DangNhap(txtUserName.Text, txtPass.Text) == true)
            {
                // bool x = false;
                MessageBox.Show("Bạn đăng nhập thành công ^^", "Thông báo", MessageBoxButtons.OK, MessageBoxIcon.Information);
                Main frm1 = new Main();
                frm1.Show();
                Hide();
            }
            else MessageBox.Show("Tên đăng nhập hoặc mật khẩu sai. Mời bạn nhập lại !!!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }
}
