// https://codingvision.net/c-simple-http-server

using System;
using System.Net;
using System.IO;
using System.Text;

namespace test
{
	class SimpleHttpServer
	{
		static void Main(string[] args)
		{
			HttpListener server = new HttpListener();
			server.Prefixes.Add("http://*:8080/");

			server.Start();
			Console.WriteLine("Listening on port 8080 ...");

			while (true)
			{
				HttpListenerContext context = server.GetContext();
				HttpListenerResponse response = context.Response;

				byte[] buffer = Encoding.UTF8.GetBytes("Hello, World!\n");
				response.ContentLength64 = buffer.Length;
				response.OutputStream.Write(buffer, 0, buffer.Length);

				context.Response.Close();
			}

		}
	}
}
