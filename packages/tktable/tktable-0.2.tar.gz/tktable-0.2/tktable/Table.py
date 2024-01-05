from ttkbootstrap import Treeview, Style

class Table(Treeview):

    def __init__(self, parent, columns:tuple, font_face="TkDefaultFont" , font_size=10,col_width=50, headings_bold=False):

        self.degree = len(columns)

        super().__init__(parent,columns=tuple(range(self.degree)), show="headings")

        self.style = Style()
        self.style.configure('Treeview',font=(font_face,font_size,""))
        self.style.configure('Treeview.Heading', font=(font_face, 12, "bold" if headings_bold else ""))

        
        for i in range(self.degree):
            super().column(i,width=col_width, anchor="center")
            super().heading(i,text=columns[i])

    def insert_row(self, row:tuple):
        if len(row) == self.degree:
            super().insert("","end",values=row)
        else:
            raise Exception("Row tuple's length is inappropriate.")