"""Visualization of the Gaussian elimination algorithm"""

__author__ = "Domen Gorjup"

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def gauss_visualize(A, b, LU=False, cmap='PRGn', float_precision=1, savepath='', fps=1):
    """
    Computation and visualization of the Gaussian elimination algorithm.

    :param A: matrix of coefficients
    :param b: vector of right-hand sides
    :param LU: if True, performs LU decomposition
    :param cmap: matplotlib cmap label, default 'PRGn'
    :param f_precision: number of decimal places for numeric values
    :param savepath: path for saving the .gif animation
    :param fps: number of frames per second of the matplotlib animation
    :return: matplotlib animation
    """
    if LU:
        mat = A
    else:
        mat = np.column_stack((A, b))

    if isinstance(mat, np.ndarray) and len(mat.shape)==2 and mat.shape[1] >= mat.shape[0]:
        colors = np.zeros_like(mat).astype(float)
        mat = mat.astype(float)
    else:
        raise Exception('Invalid data')

    color_steps = []
    mat_steps = []
    color_steps.append(colors.copy())
    mat_steps.append(mat.copy())
    L = np.zeros_like(mat) # LU decomposition

    for i in range(len(mat)-1):
        colors[i] -= 0.5
        colors[:, i] -= 0.35
        for j in range(i+1, len(mat)):
            colors[j] += 1
            m = mat[j,i]/mat[i,i]
            mat[j, i:] -= mat[i, i:]*m
            if LU:
                mat[j, i] = m

            # rows above the pivot should not be colored
            for i_without in range(i):
                colors[i_without] = 0


            # all elements that were replaced should be colored separately
            colors[np.nonzero(L)] = 0.4
            # in this step the replaced element should not yet be colored, so we save the colors above
            L[j, i] = m
            mat_steps.append(mat.copy())
            color_steps.append(colors.copy())
            colors[j] -= 1.
            colors[np.nonzero(L)] = 0.4 # this must always hold

        colors[i] += 0.5
        colors[:, i] += 0.35
        colors[np.nonzero(L)] = 0.5 # this must always hold

    # colored lower triangle
    triangle = np.zeros_like(color_steps[0])
    triangle[np.nonzero(L)] = 0.5
    color_steps.append(triangle)

    # below the diagonal are the elements of L
    if LU:
        last_step = mat_steps[-1].copy()
        last_step[np.nonzero(L)] = L[np.nonzero(L)]
        mat_steps.append(last_step)
    else:
        mat_steps.append(mat_steps[-1])

    return visualize(color_steps, mat_steps, cmap, float_precision, savepath, fps, LU), mat_steps[-1]


def visualize(colors, values=None, cmap='PRGn',f_precision=1, savepath='', fps=1, LU=False):
    """
    Visualization of the Gaussian elimination algorithm in matplotlib.

    :param colors: steps of element colors of the matrix, values [-1, 1]
    :param values: steps of values in the matrices
    :param cmap: matplotlib cmap label, default 'PRGn'
    :param f_precision: number of decimal places for numeric values
    :param savepath: path for saving the .gif animation
    :param fps: number of frames per second of the matplotlib animation
    :param LU: if True, performs LU decomposition
    :return: matplotlib animation
    """


    fig, ax = plt.subplots(1, 1)

    im = ax.imshow(colors[0], vmin=-1, vmax=1, cmap=cmap, animated=True)
    plt.axis('off')

    # text
    m_text = ax.text(-0.6, -0.8,
                    '',
                    verticalalignment='center',
                    horizontalalignment='center',
                    fontsize='x-large',
                    fontname='monospace'
                    )
    p_text = ax.text(-0.6, -1,
                    '',
                    verticalalignment='center',
                    horizontalalignment='right',
                    fontname='monospace',
                    fontsize='x-large'
                    )
    s_text = ax.text(-0.6, -0.6,
                    '',
                    verticalalignment='bottom',
                    horizontalalignment='center',
                    fontname='monospace',
                    fontsize='x-large'
                    )
    v_text = ax.text(-0.6, -1,
                    '',
                    verticalalignment='center',
                    horizontalalignment='right',
                    fontname='monospace',
                    fontsize='x-large'
                    )

    text_template = '{:.{:d}f}'
    text = []
    for i in range(values[0].shape[0]):
        for j in range(values[0].shape[1]):
            text.append(ax.text(j, i,
                                text_template.format(values[0][i, j], f_precision),
                                verticalalignment='center',
                                horizontalalignment='center',
                                fontname='monospace',
                                fontsize='large'))

    for yc in np.arange(-0.5, colors[0].shape[0], 1):
        ax.axhline(y=yc, c=(0.75, 0.75, 0.75), lw=2)
    for xc in np.arange(-0.5, colors[0].shape[1], 1):
        ax.axvline(x=xc, c=(0.75, 0.75, 0.75), lw=2)
    if not LU:
        ax.axvline(x=colors[0].shape[0]-0.5, ls='--', c='r', lw=3)

    top_line = ax.axhline(y=-0.5, lw=0.5, c='k')
    bottom_line = ax.axhline(y=0.5, lw=0.5, c='k')
    left_line = ax.axvline(x=-0.5, lw=0.5, c='k')
    right_line = ax.axvline(x=0.5, lw=0.5, c='k')

    def animate(i):
        im.set_data(colors[i])
        for t_index, t in enumerate(text):
            t.set_text(text_template.format(values[i-1].flatten()[t_index], f_precision))

        pivot = np.argmin(np.sum(colors[i], axis=1))
        row = np.argmax(np.sum(colors[i], axis=1))
        top_line.set_ydata(np.array([pivot-0.5, pivot-0.5]))
        bottom_line.set_ydata(np.array([pivot+0.5, pivot+0.5]))
        left_line.set_xdata(np.array([pivot-0.5, pivot-0.5]))
        right_line.set_xdata(np.array([pivot+0.5, pivot+0.5]))

        if i == len(colors)-1:
            p_text.set_text('')
            s_text.set_text('')
            v_text.set_text('')
            m_text.set_text('')
            top_line.set_ydata(np.array([-1.5, -1.5]))
            bottom_line.set_ydata(np.array([-1.5, -1.5]))
            left_line.set_xdata(np.array([-1.5, -1.5]))
            right_line.set_xdata(np.array([-1.5, -1.5]))

        else:
            p_text.set_text('i = {}'.format(pivot))
            p_text.set_y(pivot)
            s_text.set_text('i = {}'.format(pivot))
            s_text.set_x(pivot)
            v_text.set_text('j = {}'.format(row))
            v_text.set_y(row)
            m_text.set_text('m = {:.2f}'.format(values[i-1][row, pivot]/values[i-1][pivot, pivot]))
        return im, p_text, s_text, v_text, text, m_text, top_line, bottom_line, left_line, right_line

    ani = animation.FuncAnimation(fig, animate, np.arange(1, len(colors)),
                            interval=1000/fps, blit=True)
    if savepath:
        writer = animation.PillowWriter(fps=fps, loop=0)
        ani.save(savepath, writer)

    return
