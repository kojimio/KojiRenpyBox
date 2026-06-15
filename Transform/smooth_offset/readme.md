Smooth Offset
---

为移动速度较慢的坐标变换效果坐标被取整导致卡顿时的一个解决方案

<img src="readme.gif" height="200" />


写在前面
---

在我们写与坐标变换有关的转场的时候, 时常会装一些移动速度较慢的效果. 由于 renpy 的坐标计算机制是取整的, 所以这会导致图像变换会出现过了两三帧后直接往侧边移动一个像素点的画面, 这样的显示效果及其生硬与简陋

既然没办法改变 Renpy Transform 中对坐标的强制取整, 那我们可以非整型坐标的渲染方案就好了, 那么答案就呼之欲出了: 用 Shader 渲染. 着色器的渲染是完全基于浮点计算的, 所以自然就可以绕开整型的限制, 让画面呈现出平滑移动的效果了

Shader 的源码并没有好讲解的点, 用一个 u_animation 来将坐标从相对坐标过渡到目标位置, 这里需要讲一下的是它在 transform 中的特性

说明
---

```python  
transform smooth_offset(time, offset):
    mesh True
    shader "smooth_offset"
    u_animation 0.0
    u_pos offset
    linear time u_animation 1.0
    shader None
```

transform 传参:
- time: 动画的时间
- offset: 位移的相对坐标

transform 内:
- u_pos 为在当前位置下相对位移的终点坐标
- u_animation 为从起始坐标到终点坐标转换的动画轴

**注意:**
- 在 transform 内, 图片的坐标**并没有发生任何的变换**, 它仅仅是在原本的坐标上用 shader 画出了位移
- 在动画结束的时候, 会自动清除掉这个 shader, 此时如果不改变坐标的话, **图片会返回动画前的位置**

使用例
---

假如我们希望将以下动画变得平滑
```renpy
label test_label:
    show a:
        xpos 15
        linear 8.5 xpos 175 
```

可以这样子调用 smooth_offset

```renpy
label test_label:
    show a:
        # 动画的起始坐标
        xpos 15

        # 调用 shader 绘制出从 xpos 15 向右移动到 xpos 175 的动画
        # 也就是在 xpos 15 的位置上绘制出向右移动 xpos 175-15 的动画
        # 在此过程中并不会修改 xpos 的坐标, 仅仅是绘制出动画
        smooth_offset(8.5, (175-15, 0))

        # 动画结束, 将最终的坐标更正为终点坐标
        xpos 175 
```

附
---

如果每一次的 smooth_offset 后修改的值都是一个起始为 0 值, 也许可以考虑把 offset 的设置加到 transform 里减少演出代码? 或者加上 start_offset 什么的也可以做到较好的适配

如果希望做出自由的坐标变换效果, 可以试试看把 u_animation 始终设为 1, 然后直接更改 u_pos 呢? 

其实 renpy 里面的 xpos 在 linear 的时候也是以浮点计算的, 只是在最终渲染的时候取整了而已

这个效果的基础源码是在 renpy 预设效果里拉出来该两个字实现的
