# 锦鲤界部署指南 — GitHub Pages

> **目标**：将锦鲤界的310个HTML页面部署到免费的互联网空间，让测试人员可以通过浏览器访问。
> **推荐方案**：GitHub Pages（免费、稳定、永久、支持自定义域名）
> **部署时间**：约10分钟
> **预计访问地址**：`https://你的用户名.github.io/goi-world/`

---

## 第一步：注册 GitHub 账户（3分钟）

1. 打开 [https://github.com/signup](https://github.com/signup)
2. 输入邮箱 → 创建密码 → 设置用户名
3. 验证邮箱（查收验证邮件并点击链接）
4. 登录 GitHub

> 💡 用户名建议使用英文，如 `koi-master` 或 `jinli-zong`

---

## 第二步：添加 SSH 密钥到 GitHub（2分钟）

1. 打开 GitHub 网站 → 点击右上角头像 → **Settings**
2. 左侧菜单选择 **SSH and GPG keys**
3. 点击绿色按钮 **New SSH key**
4. **Title** 填：`锦鲤界部署`
5. **Key** 填：以下公钥（请完整复制）

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOWstdeYoa0+EMC22lBB+DRk/dwF71AKezlYtgXtroSk 锦鲤界部署
```

> 或者打开本目录下的 `SSH_PUBLIC_KEY.txt` 文件复制

6. 点击 **Add SSH key**

---

## 第三步：在 GitHub 创建仓库（1分钟）

1. 打开 [https://github.com/new](https://github.com/new)
2. **Repository name** 填：`goi-world`
3. 选择 **Public**（公开）
4. 不要勾选 "Add a README file"
5. 点击 **Create repository**

---

## 第四步：推送代码到 GitHub（3分钟）

打开 **Git Bash**（或命令行），执行以下命令：

```bash
# 进入锦鲤界目录
cd "D:/Data/-= AI/20260700 - 锦鲤宗宗门建设/01 - IP建设/锦鲤界"

# 添加远程仓库（将 chinacamel78 替换为你的 GitHub 用户名）
git remote add origin git@github.com:chinacamel78/goi-world.git

# 推送代码
git push -u origin master
```

> 第一次推送时可能会提示确认主机指纹，输入 `yes` 回车即可。

---

## 第五步：启用 GitHub Pages（1分钟）

1. 打开你的仓库页面：`https://github.com/chinacamel78/goi-world`
2. 点击顶部菜单 **Settings**（⚙️）
3. 左侧菜单选择 **Pages**
4. **Source** 选择 **Deploy from a branch**
5. **Branch** 选择 **master** → **/(root)** → 点击 **Save**

---

## 第六步：访问锦鲤界！

等待约1-2分钟后，打开以下地址：

```
https://chinacamel78.github.io/goi-world/
```

> 将 `chinacamel78` 替换为你的 GitHub 用户名。

---

## 维护信息

| 项目 | 内容 |
|------|------|
| **总页面数** | 310 个 HTML 页面 |
| **总文件数** | 314 个文件 |
| **总大小** | 约 2.1 MB |
| **本地路径** | `D:/Data/-= AI/20260700 - 锦鲤宗宗门建设/01 - IP建设/锦鲤界/` |
| **Git 分支** | `master` |
| **SSH 密钥** | `~/.ssh/id_ed25519` |
| **部署方式** | GitHub Pages（免费） |
| **更新方式** | 修改本地文件 → `git add .` → `git commit -m "更新说明"` → `git push` |

---

## 后续更新操作

当内容需要更新时，执行以下命令：

```bash
cd "D:/Data/-= AI/20260700 - 锦鲤宗宗门建设/01 - IP建设/锦鲤界"
git add .
git commit -m "更新内容：xxx"
git push
```

> GitHub Pages 会自动重新部署，约1-2分钟后生效。

---

## 备选方案

如果 GitHub Pages 不适合，以下是其他免费托管方案：

| 方案 | 特点 | 部署方式 |
|------|------|---------|
| **Vercel** | 自动部署，支持预览 | 从 GitHub 仓库导入 |
| **Cloudflare Pages** | 全球CDN加速 | 从 GitHub 仓库导入 |
| **Netlify** | 拖拽上传，简单 | 拖拽文件夹上传 |
| **Surge.sh** | 命令行快速部署 | `npx surge` |

---

## 技术支持

- GitHub 文档：[https://docs.github.com/cn/pages](https://docs.github.com/cn/pages)
- SSH 问题排查：[https://docs.github.com/cn/authentication/troubleshooting-ssh](https://docs.github.com/cn/authentication/troubleshooting-ssh)

---

> 🎏 **锦鲤不是天生好运，而是底层思考带来的必然。**
