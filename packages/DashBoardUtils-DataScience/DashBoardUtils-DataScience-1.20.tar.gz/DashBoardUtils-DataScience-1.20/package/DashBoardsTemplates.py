# bokeh version

from bokeh.plotting import figure
import random
import math


def export_graphs_hist(chuncks):
    obj_lists = []
    for i, x in enumerate(chuncks):
        fruits = list(x.values())[0]["lables"]
        counts = list(x.values())[0]["counts"]
        p = figure(
            x_range=fruits,
            height=350,
            title=list(x.keys())[0],
            toolbar_location=None,
            tools="",
        )
        p.vbar(x=fruits, top=counts, width=0.9)
        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        obj_lists.append(p)
    return "exported {}".format(str(len(chuncks))), obj_lists


def export_graphs_line(chuncks):
    obj_lists = []
    for i, x in enumerate(chuncks):
        fruits = [x for x in range(len(list(x.values())[0]["lables"]))]
        counts = list(x.values())[0]["counts"]
        graph = figure(title=list(x.keys())[0])
        graph.line(fruits, counts, line_width=2)
        graph.xaxis.axis_label = ",".join(list(x.values())[0]["lables"])
        obj_lists.append(graph)
    return "exported {}".format(str(len(chuncks))), obj_lists


def export_graphs_pie_charts(chuncks):
    obj_lists = []
    for i, x in enumerate(chuncks):
        graph = figure(title=list(x.keys())[0])
        sectors = list(x.values())[0]["lables"]
        percentages = list(x.values())[0]["counts"]
        radians = [math.radians((percent / 100) * 360) for percent in percentages]
        start_angle = [math.radians(0)]
        prev = start_angle[0]
        for i in radians[:-1]:
            start_angle.append(i + prev)
        prev = i + prev
        end_angle = start_angle[1:] + [math.radians(0)]
        x = 0
        y = 0
        radius = 1
        color = [
            "#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])
            for i in range(len(sectors))
        ]
        for i in range(len(sectors)):
            graph.wedge(
                x,
                y,
                radius,
                start_angle=start_angle[i],
                end_angle=end_angle[i],
                color=color[i],
                legend_label=sectors[i],
            )
        obj_lists.append(graph)
    return "exported {}".format(str(len(chuncks))), obj_lists


def data_verience_whole_table(chuncks):
    newlist = [list(x.keys())[0] for x in chuncks]
    return {i: newlist.count(i) for i in newlist}


def build_dogged_from(data, title):
    from bokeh.plotting import figure
    from bokeh.models import ColumnDataSource, FactorRange

    label_data = data[list(data.keys())[0]]
    catagories = list(data.keys())[1:]
    sq = []
    x = [(label, catagory) for label in label_data for catagory in catagories]
    counts = sum(zip(*[data[xa] for xa in catagories]), ())
    source = ColumnDataSource(data=dict(x=x, counts=counts))
    p = figure(
        x_range=FactorRange(*x),
        height=500,
        title=title,
        toolbar_location=None,
        tools="",
        output_backend="svg"
        ,width=1000,
    )
    p.vbar(x="x", top="counts", width=0.9, source=source, line_color="white")
    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None
    return p


def export_graphs_nested_color_mapped(chuncks):
    ploat_ = [(list(x.keys())[0], list(x.values())) for x in chuncks]
    import collections

    c = collections.defaultdict(list)
    for a, b in ploat_:
        c[a].extend(b)  # add to existing list or create a new one

    list_2 = list(c.items())
    label_unique = []
    for xs in list_2:
        for xp in xs[1]:
            label_unique += xp["lables"]
    core_labels = [x[0] for x in ploat_]
    dummy_label_list = {}
    for x in list(set(label_unique)):
        dummy_label_list[x] = [pr for pr in range(len([x[0] for x in ploat_]))]
    final_data = {"core": list(set(core_labels))}
    for im, x in enumerate(list(set(core_labels))):
        dummy_labels = []
        for d in ploat_:
            if d[0] == x:
                dummy_labels.append(d)
        dummy_labels_to_dict = collections.defaultdict(list)
        for p, m in dummy_labels:
            dummy_labels_to_dict[p].extend(m)
        listw = list(dummy_labels_to_dict.items())
        for sx in listw:
            data23 = {"lables": [], "counts": []}
            formatted = {}
            for xsd in sx[1]:
                data23["lables"] += xsd["lables"]
                data23["counts"] += xsd["counts"]
            for xw in range(len(data23["lables"])):
                if list(formatted.keys()) == []:
                    formatted[data23["lables"][xw]] = data23["counts"][xw]
                if data23["lables"][xw] not in list(formatted.keys()):
                    formatted[data23["lables"][xw]] = data23["counts"][xw]
                else:
                    formatted[data23["lables"][xw]] += data23["counts"][xw]
            corew = []
            for xsww in core_labels:
                if xsww not in corew:
                    corew.append(xsww)
            datasq = {}
            for k, v in formatted.items():
                index = corew.index(sx[0])
                dummy_lab = [0 for x in corew]
                dummy_lab[index] = v
                datasq[k] = dummy_lab
            final_data.update(datasq)
    return (
        "exported {}".format(str(len(chuncks))),
        build_dogged_from(final_data, "Test Title"),
    )
