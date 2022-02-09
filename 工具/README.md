本目录整理一些开发工具

# 1. Git
[git](./git.md)：代码版本管理工具

# 2. Genymotion
[genymotion](./genymotion.md)：手机模拟器

# 3. Powershell
> window上比较好用的终端

增强使用，例如git补全和颜色等：https://zhuanlan.zhihu.com/p/137251716

# 4. iTerm2
参考：[安装及使用基础plugins](https://makeoptim.com/tool/terminal#iterm2)
参考：[vscode终端适配](https://saiankit30.medium.com/how-to-change-the-integrated-terminal-in-vs-code-from-default-to-pro-iterm-ish-5c958e13aada)
参考：[干掉分支修改统计](https://stackoverflow.com/questions/59500000/i-have-a-problem-with-it-when-i-use-powerlevel10k-which-is-a-theme-for-zsh)
参考：[主题选择](https://github.com/ohmyzsh/ohmyzsh/wiki/Themes)
mac 好用的终端工具，一般需要配置以下东西

> 是我的错觉吗？这个终端似乎反应有点慢？

- [x] 安装主题，新设备可从上面的配置文件导入```~/.p10k.zsh```
- [x] 安装oh-my-zsh、aotojump、autosuggestion
- [x] 设置为默认终端
- [x] 跟pycharm或者vscode兼容
- [x] git自动补全(zsh)：将```autoload -Uz compinit && compinit```添加到zshrc

> Never use source ~/.zshrc. Use exec zsh instead. It's shorter and much less likely to break your shell
>
> 确定吗？-_-?

>oh-my-zsh，oh-my-posh是啥关系？

```
# 重新配置
p10k configure
# tab之后补全，如果有多个可能的选择，双击tab切换
```

## 待整理

- zookeeper
- rancher
- k8s

### 压测
ab：https://segmentfault.com/a/1190000020211494
```
ab -c 10 -n 50 -k http://45.77.104.12:5057/
-c: 并发数
-n: 请求总数
-k: keep-alive
```

## 
