<h2>DarkPyro-REV</h2>
<p>Just Kanger Userbot<p>

<h2>About</h2>
<p>DarkPyro-REV is a Telegram userbot (in case you didn't know, selfbot/userbot are used to automate user accounts). So how does it work? It works in a very simple way, using the pyrogram library, a python script connects to your account (creating a new session) and catches your commands.

Using selfbot/userbot is against Telegram's Terms of Service, and you may get banned for using it if you're not careful.

We are not responsible for any consequences you may encounter when using DarkPyro-REV. We are also not responsible for any damage to chat rooms caused by
using this userbot.</p>


<h2>Disclaimer (Indonesian)</h2>
<p>
(A) Repo sepenuhnya bukan hasil karya kami, melainkan hanya mengedit dari sebagian repo userbot.
(B) Kami tidak menyarankan Anda untuk menggunakan repo kami di akun utama.
(C) Hindari untuk menggunakan modul pesan siaran (broadcast) terlalu sering, jika memungkinkan jangan digunakan.
</p>

<p>
<b>Catatan:</b>
1) Kami tidak menambahkan daftar hitam,
2) Jika dikemudian hari akun Anda diban di beberapa grup dan mengalami limit oleh <a href='https://t.me/SpamBot'>@SpamBot</a> atau lebih fatalnya akun Anda dibanned oleh telegram (Silahkan baca kembali poin B, C)
</p>

<p>
<b>Tambahan:</b>
Kami menambahkan command <code>devil</code> [<a
href='https://github.com/2R-Dark-Kanger-Pro/DarkPyro-REV/blob/64e762f4e27aeed23a3109ac91ec3e99caa5d1d6/ProjectDark/modules/network.py#L27'>Read Code</a>] untuk memudahkan mengecek user yang menggunakan userbot, dan hanya bekerja jika anda bergabung di grup support kami.
</p>


<h2>Deploy on VPS</h2>
<h4>1. Install docker-compose & git</h4>
<pre><code>sudo su && apt -y install git docker-compose</code></pre>

<h4>2. Clone Repository</h4>
<pre><code>git clone https://github.com/2R-Dark-Kanger-Pro/deploy</code></pre>

<h4>3. cd dir & cp sample config</h4>
<pre><code>cd deploy && cp config.env_sample config.env</code></pre>

<h4>4. Edit config.env</h4>
<pre><code>nano config.env</code></pre>
<p>Save it with Ctrl S + Ctrl X</p>

<h4>5. docker compose up</h4>
<pre><code>docker-compose up --build -d</code></pre>

<h4>6. Get logs compose</h4>
<pre><code>docker-compose logs -f</code></pre>


<h2>Group Discussion</h2>
<p><a href='https://t.me/DarkPyroREV'>Telegram</a></p>


<h2>Credits</h2>
<nav>
<li><a href='https://github.com/mrismanaziz/PyroMan-Userbot'>PyroMan-Userbot</a> Base</li>
<li><a href='https://github.com/Dragon-Userbot/Dragon-Userbot'>Dragon-Userbot</a></li>
</nav>

<h4>Written on <a
href='https://github.com/pyrogram/pyrogram'>Pyrogram️</a></h4>
