def getNode(name, l): #回傳在列表l內對應name的NODE物件
   return next(( i for i in l if i.name == name), -1)