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
    public partial class frmNhanVien : Form
    {
        public frmNhanVien()
        {
            InitializeComponent();
        }
        BUS_NhanVien nhanvien = new BUS_NhanVien();
        int chon = 0;
        TimKiem tk = new TimKiem();
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
        void SetNull()
        {
            txtMaNV.Text = txtHoDem.Text = txtTenNV.Text = txtGT.Text = txtSDT.Text = txtDiaChi.Text = txtLuong.Text = "";
            txtChucVu.Text = cbMa_NQL.Text = cbMaDV.Text = "";
            dtpNgaySinh.Text = DateTime.Now.ToShortDateString();
            tscbGT.Text = tstxtDiaChi.Text = tstxtMa.Text = tstxtTen.Text = "";
        }


        private void frmNhanVien_Load(object sender, EventArgs e)
        {
            DataTable dt = new DataTable();
            dt = nhanvien.HienThiNhanVien();
            dgvNhanVien.DataSource = dt;
            KhoaDieuKhien();
            
        }

    }
}
