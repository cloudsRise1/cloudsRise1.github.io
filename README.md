# 个人主页

在线主页：[cloudsrise1.github.io](https://cloudsrise1.github.io/) · 源码仓库：[cloudsRise1/cloudsRise1.github.io](https://github.com/cloudsRise1/cloudsRise1.github.io)

面向 GitHub Pages 的独立静态个人主页，使用原生 HTML、CSS 和 JavaScript，不依赖前端框架、包管理器或第三方 Python 包。`profile.json` 保存个人资料，`build.py` 使用 Python 标准库生成站点，并支持可选的 `--output` 参数。

包含完整网页、可编辑资料、原生交互、移动端样式、404 页面与 GitHub Pages 自动部署工作流。无需数据库和 API key。

## 设计与身份

当前排版参考 [hbx-hbx.github.io](https://hbx-hbx.github.io/)：白色背景、左侧常驻个人资料、右侧正文、蓝色链接、带图标的章节标题与紧凑论文列表。手机端个人资料置顶，导航可横向滚动。仅借鉴排版，不复制参考站的肖像或个人履历。

当前使用已授权的 GitHub 用户名 `cloudsRise1`；姓名、邮箱、论文和履历可在 `profile.json` 中补充。简介为按研究方向起草的文字，可自行调整。

## 本地预览

需要 Python 3；CI 使用 Python 3.12。无需执行 `pip install` 或安装 Node.js。

在项目根目录运行：

```bash
python3 build.py
python3 -m http.server 8000
```

打开 <http://localhost:8000/>。第一个命令使用生成器的默认输出位置，第二个命令启动当前目录的静态文件服务；按 `Ctrl+C` 停止服务。

也可以指定独立输出目录，与 CI 保持一致：

```bash
python3 build.py --output _site
python3 -m http.server 8000 --directory _site
```

`_site/` 是生成产物，已加入 `.gitignore`。根目录的 `.nojekyll` 是静态站点标记；Actions 工作流直接上传生成目录，不执行 Jekyll。

## 修改资料

编辑 `profile.json` 中站点实现定义的字段，填写自己的资料，然后重新运行 `python3 build.py`。更换照片或其他资源时，将文件放入 `assets/` 并同步更新资料中的相对路径。

保持 JSON 语法有效，不添加注释或末尾多余的逗号。主页生成后是公开内容；不要在资料、网页或资源中放入密码、令牌、私钥或未获授权的个人信息。`.gitignore` 不能代替内容检查。

## GitHub Pages

支持两种仓库形式：

- 用户主页：仓库名为 `USERNAME.github.io`，访问地址为 `https://USERNAME.github.io/`。
- 项目主页：仓库名例如 `personal-homepage`，访问地址为 `https://USERNAME.github.io/personal-homepage/`。

将 `USERNAME` 替换为实际 GitHub 用户名。为兼容项目路径，站点实现中的样式、脚本、图片和内部链接应使用相对路径，例如 `assets/style.css`，避免以 `/assets/` 这样的域名根路径开头。`--output _site` 只指定构建目录，不会自动修正资源 URL。

本站采用 **Settings → Pages → Deploy from a branch → main / (root)** 发布根目录的 `index.html`。本地修改 `profile.json` 后运行 `python3 build.py`，将更新的配置和网页推送到 `main`，GitHub Pages 会自动重新发布。

源码包额外提供可选的 Actions 构建工作流，当前线上仓库使用主分支发布方式。若要启用自动资料构建，将 `.github/workflows/pages.yml` 上传到仓库（GitHub CLI 需要 `workflow` scope），再将 **Build and deployment → Source** 设为 **GitHub Actions**；此时只修改 `profile.json` 并推送即可自动生成网页并部署，也可以在 **Actions → Deploy GitHub Pages → Run workflow** 手动触发。

工作流只使用 GitHub 官方稳定版本的 Actions：检出源码、配置 Python、配置 Pages、上传 `_site/`，最后部署到 `github-pages` 环境。它授予 `contents: read`、`pages: write`、`id-token: write` 权限；部署并发组为 `pages`，不会取消正在执行的部署。

### 仓库命令示例

以下为首次部署命令。需要已安装并登录 GitHub CLI。公开仓库会公开源码，包括 `profile.json`。

用户主页示例，假设这是尚未初始化 Git 的新目录：

```bash
cd /Users/bytedance/项目/personal-homepage
gh auth login
git init -b main
git add README.md CONTENT_GUIDE.md .gitignore .nojekyll .github/workflows/pages.yml build.py profile.json index.html 404.html assets/
git commit -m "Initialize personal homepage"
gh repo create USERNAME.github.io --public --source=. --remote=origin
git push -u origin main
```

项目主页使用相同的初始化、检查和提交步骤，将创建仓库的命令替换为：

```bash
gh repo create personal-homepage --public --source=. --remote=origin
git push -u origin main
```

创建仓库后，按前述说明选择主分支或可选的 GitHub Actions 作为 Pages 来源。
