from lxml import etree
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

#------------------------------------------------------------------------#
def make_graph(year):
    # イテレータで逐次パース
    context = etree.iterparse("dblp.xml", events=("end",), load_dtd=True, resolve_entities=True)

    G = nx.Graph() 
    node_author = []

    i = 0

    for event, elem in context:
        # 出版されたものだけを処理
        if elem.tag == "article" and len(elem) > 1:
            flag = True
            # XMLの文字列として整形して出力
            # print(etree.tostring(elem, pretty_print=True, encoding="unicode"))
            for child in elem:
                if child.tag == "author":
                    node_author.append(child.text)
                if child.tag == "title":
                    print(child.text)
                if child.tag == "year" and int(child.text) == year:
                    print(child.text)
                    flag = False
                
            if flag:
                print("指定した年代のデータではありません")
                # メモリ節約
                node_author.clear()
                elem.clear()
                continue
                
            index = 1
            for u in range(0,len(node_author)):
                if u == len(node_author)-1:
                    break
                for v in range(index,len(node_author)):
                    G.add_edge(node_author[u], node_author[v])
                index += 1
                    
            print(node_author)
            
            # メモリ節約
            node_author.clear()
            elem.clear()
            
            i += 1
        
        if i == 10:
            break

    # サブグラフプロット
    plt.figure(figsize=(4, 3), dpi=300) 
    pos = nx.spring_layout(G, k=0.1, iterations=50)
    nx.draw_networkx(G, pos,
                     node_size = 2,
                     node_color = 'skyblue',
                     edge_cmap = plt.cm.RdBu_r,
                     with_labels = False,
                     font_size = 2,
                     font_color = 'black',
                     width = 0.2)

    # 黒い枠（スプライン）を消す
    ax = plt.gca()  # 現在の軸を取得
    for spine in ax.spines.values():  # スプライン（外枠）を非表示
        spine.set_visible(False)

    plt.show()
    
make_graph(2024)
    


    
        
    
