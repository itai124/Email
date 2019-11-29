using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Email_client
{
    public partial class Form1 : Form
    {
        private Socket send;
        private IPEndPoint remoteEP;
        private byte[] bytes;
        public Form1()
        {
            InitializeComponent();
            byte[] bytes = new byte[1024];
            IPHostEntry ipHostInfo = Dns.Resolve(Dns.GetHostName());
            IPAddress ipAddress = ipHostInfo.AddressList[0];
            IPEndPoint remoteEP = new IPEndPoint(ipAddress, 11000);
            Socket send = new Socket(AddressFamily.InterNetwork,
            SocketType.Stream, ProtocolType.Tcp);

        }


        private void button1_Click(object sender, EventArgs e)
        {
            send.Connect(remoteEP);
            Console.WriteLine("connected");
            string ip = this.IpBox.Text;
            string subject = this.SubjectBox.Text;
            string text = this.TextBox.Text;
            this.IpBox.Text = null;
            this.SubjectBox.Text = null;
            this.TextBox.Text = null;
            Console.WriteLine("send ip");
            byte[] msg = Encoding.ASCII.GetBytes(ip);
            int bytesSent = send.Send(msg);
            int bytesRec = send.Receive(bytes);
            Console.WriteLine("Echoed test = {0}",
            Encoding.ASCII.GetString(bytes, 0, bytesRec)); 
            Console.WriteLine("send subject");
            byte[] msg2 = Encoding.ASCII.GetBytes(subject);
            int bytesSent2 = send.Send(msg2);
            int bytesRec2 = send.Receive(bytes);
            Console.WriteLine("Echoed test = {0}",
            Encoding.ASCII.GetString(bytes, 0, bytesRec2));
            Console.WriteLine("send text");
            byte[] msg3 = Encoding.ASCII.GetBytes(text);
            int bytesSent3 = send.Send(msg3);
            int bytesRec3 = send.Receive(bytes);
            Console.WriteLine("Echoed test = {0}",
            Encoding.ASCII.GetString(bytes, 0, bytesRec3));

        }
    }
    
}
