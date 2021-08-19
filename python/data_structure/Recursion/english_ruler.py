def  draw_line(tick_length,tick_lable=''):
    """draw the line with given tick length"""
    line ='-'* tick_length
    if tick_lable:
        line+=' ' + tick_lable
    print(line)

def draw_interval(center_length):
    if center_length >0:
        draw_interval(center_length-1)
        draw_line(center_length)
        draw_interval(center_length-1)

def draw_ruler(num_inches,major_lenghth):
    draw_line(major_lenghth,'0')
    for j in range(1 ,1+num_inches):
        draw_interval(major_lenghth-1)
        draw_line(major_lenghth,str(j))


draw_interval(4)