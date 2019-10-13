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
    public partial class frmNhanVien : Form
    {
        public frmNhanVien()
        {
            InitializeComponent();
        }
        void KhoaDieuKhien()
        {
            txtMaNV.Enabled = txtHoDem.Enabled = txtTenNV.Enabled = txtGT.Enabled = dtpNgaySinh.Enabled = txtDiaChi.Enabled = txtSDT.Enabled = txtLuong.Enabled = txtChucVu.Enabled = cbMa_NQL.Enabled = cbMaDV.Enabled = false;
            btnThem.Enabled = btnSua.Enabled = btnXoa.Enabled = true;
            btnLuu.Enabled = false;
        }
        void MoDieuKhien()
        {
            txtMaNV.Enabled = txtHoDem.Enabled = txtTenNV.Enabled = txtGT.Enabled = dtpNgaySinh.Enabled = txtDiaChi.Enabled = txtSDT.Enabled = txtLuong.Enabled = txtChucVu.Enabled = cbMa_NQL.Enabled = cbMaDV.Enabled = true;
            btnThem.Enabled = btnSua.Enabled = btnXoa.Enabled = false;
            btnLuu.Enabled = true;
        }

    }
}
