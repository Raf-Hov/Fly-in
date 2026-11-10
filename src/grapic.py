import matplotlib.pyplot as plt
from matplotlib.colors import is_color_like
from .structes import MapData, Zone, Connection, ZoneTypes
from matplotlib.lines import Line2D


class MapVisualizer:
    DEFAULT_COLOR = "lightgray"
    TYPE_MARKS = {
        ZoneTypes.NORMAL: "o",
        ZoneTypes.PRIORITY: "*",
        ZoneTypes.RESTRICTED: "s",
        ZoneTypes.BLOCKED: "X",
    }
    START_MARKER = "D"
    END_MARKER = "p"

    def __init__(self, data: MapData) -> None:
        self.data: MapData = data

    @staticmethod
    def _zone_color(zone: Zone) -> str:
        if zone.color is not None and is_color_like(zone.color):
            return zone.color
        return MapVisualizer.DEFAULT_COLOR

    def _zone_marker(self, zone: Zone) -> str:
        if zone.is_start:
            return self.START_MARKER
        if zone.is_end:
            return self.END_MARKER
        return self.TYPE_MARKS[zone.zone_type]

    def _figure_size(self) -> tuple[float, float]:
        xs = [z.x for z in self.data.zones.values()]
        ys = [z.y for z in self.data.zones.values()]
        width = max(7.0, (max(xs) - min(xs)) * 1.6 + 2)
        height = max(4.5, (max(ys) - min(ys)) * 1.4 + 3)
        return width, height

    def _drow_connection(self, ax: plt.Axes, link: Connection) -> None:
        a = self.data.zones[link.zone1]
        b = self.data.zones[link.zone2]
        cap = link.max_link_capacity
        ax.plot(
            [a.x, b.x], [a.y, b.y],
            color="grey", zorder=1,
            linewidth=1.2 + 0.6 * min(cap - 1, 4))
        if cap > 1:
            ax.text((a.x + b.x) / 2, (a.y + b.y) / 2, str(cap),
                    fontsize=7, ha="center", va="center", zorder=2,
                    bbox={"boxstyle": "round,pad=0.15", "fc": "white",
                          "ec": "gray", "lw": 0.5})

    def _drow_zone(self, ax: plt.Axes, zone: Zone) -> None:
        ax.scatter([zone.x], [zone.y], s=320, zorder=3,
                   marker=self._zone_marker(zone),
                   c=self._zone_color(zone), edgecolors="black")
        label = zone.name
        if zone.capacity is not None and zone.capacity > 1:
            label += f" ({zone.capacity})"
        ax.annotate(label, (zone.x, zone.y), xytext=(0, 14),
                    textcoords="offset points", ha="center",
                    fontsize=7, zorder=4)

    def _draw_legend(self, sef, ax: plt.Axes) -> None:
        items = [("start", self.START_MARKER), ("end", self.END_MARKER),
                 ("normal", "o"), ("priority", "*"),
                 ("restricted", "s"), ("blocked", "X")]
        handles = [Line2D([], [], marker=m, linestyle="", color="gray",
                          markeredgecolor="black", label=name)
                   for name, m in items]
        ax.legend(handles=handles, loc="upper center",
                  ncol=6, fontsize=7, frameon=False)

    def draw_map(self) -> plt.Figure:
        fig, ax = plt.subplot(figsize=self._figure_size())
        for link in self.data.connections:
            self._draw_connection(ax, link)
        for zone in self.data.zones.values():
            self._draw_zone(ax, zone)
        self._draw_legend(ax)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(f"{self.data.nb_drones} drones", pad=18)
        return fig

    def show(self) -> None:
        self.draw_map()
        plt.show()
