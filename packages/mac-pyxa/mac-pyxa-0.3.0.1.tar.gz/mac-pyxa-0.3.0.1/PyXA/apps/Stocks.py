""".. versionadded:: 0.0.6

Control the macOS Stocks application using JXA-like syntax.
"""

from typing import Union
from AppKit import NSPredicate, NSMutableArray, NSURL

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XAClipboardCodable


class XAStocksApplication(XABase.XAApplication):
    """A class for managing and interacting with Stocks.app.

    .. seealso:: :class:`XAStocksSavedStock`

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def sidebar_showing(self) -> bool:
        """Whether the sidebar is currently showing."""
        sidebar = (
            self.front_window.xa_elem.groups()[0]
            .groups()[0]
            .groups()[0]
            .groups()[0]
            .groups()[0]
            .groups()[1]
            .groups()[0]
            .groups()[0]
            .groups()[1]
        )
        return sidebar.get() is not None

    def show_symbol(self, ticker: str) -> "XAStocksApplication":
        """Displays the page for the specified ticker symbol.

        :param ticker: The ticker symbol for the desired stock
        :type ticker: str
        :return: A reference to the application object
        :rtype: XAStocksApplication

        .. versionadded:: 0.0.6
        """
        XABase.XAURL("stocks://?symbol=" + ticker).open()

    def go_back(self) -> "XAStocksApplication":
        """Clicks the 'back' button (from a new article when viewed in the Stocks app).

        :return: A reference to the application object
        :rtype: XAStocksApplication

        .. versionadded:: 0.0.6
        """
        self.front_window.toolbars()[0].buttons()[0].actions()[0].perform()
        return self

    def show_business_news(self) -> "XAStocksApplication":
        """Shows the 'Business News' tab in the front stock window.

        :return: A reference to the application object
        :rtype: XAStocksApplication

        .. versionadded:: 0.0.6
        """
        self.front_window.groups().at(0).groups().at(0).groups().at(0).groups().at(
            0
        ).groups().at(0).groups().at(0).groups().at(0).groups().at(1).groups().at(
            0
        ).groups().at(
            0
        ).groups().at(
            0
        ).groups().at(
            0
        ).groups().at(
            0
        ).groups().at(
            0
        ).groups().at(
            0
        ).groups().at(
            1
        ).groups().at(
            0
        ).groups().at(
            0
        ).groups().at(
            1
        ).groups().at(
            0
        ).ui_elements().at(
            2
        ).buttons().at(
            0
        ).actions()[
            0
        ].perform()

    def new_tab(self):
        """Opens a new tab.

        .. versionadded:: 0.0.6
        """
        predicate = NSPredicate.predicateWithFormat_("name == %@", "AXPress")
        press_action = (
            self.front_window.xa_elem.tabGroups()[0]
            .buttons()[0]
            .actions()
            .filteredArrayUsingPredicate_(predicate)[0]
        )
        press_action.perform()

    def saved_stocks(self) -> "XAStocksSavedStockList":
        """Gets a list of stocks.

        :return: The list of stocks
        :rtype: XAStocksStockList

        .. versionadded:: 0.0.6
        """
        stock_element_list = (
            self.front_window.xa_elem.groups()[0]
            .groups()[0]
            .groups()[0]
            .groups()[0]
            .groups()[0]
            .groups()[0]
            .groups()[0]
            .groups()[1]
            .groups()[0]
            .groups()[0]
            .groups()[0]
            .groups()[0]
            .groups()[0]
            .groups()[0]
            .groups()[0]
            .groups()[1]
            .groups()[0]
            .groups()[0]
            .groups()[1]
            .groups()[0]
            .groups()
        )

        stocks = []

        def add_stock(element, index, stop):
            nonlocal stocks
            groups = element.groups()
            if len(groups) == 1:
                stocks.append(groups[0].UIElements()[0])

        stock_element_list.enumerateObjectsUsingBlock_(add_stock)

        return self._new_element(
            NSMutableArray.alloc().initWithArray_(stocks), XAStocksSavedStockList
        )


class XAStocksSavedStockList(XABase.XAList, XAClipboardCodable):
    """A wrapper around a list of stocks.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAStocksSavedStock, filter)

    def properties(self) -> list[str]:
        return self.xa_elem.arrayByApplyingSelector_("properties")

    def name(self) -> list[str]:
        return [x.name for x in self]

    def symbol(self) -> list[str]:
        return [x.symbol for x in self]

    def price(self) -> list[str]:
        return [x.price for x in self]

    def change(self) -> list[str]:
        return [x.change for x in self]

    def selected(self) -> list[str]:
        ls = self.xa_elem.arrayByApplyingSelector_("selected")
        return [x.get() for x in ls]

    def get_clipboard_representation(self) -> list[Union[str, NSURL]]:
        """Gets a clipboard-codable representation of each stock in the list.

        When the clipboard content is set to a list of saved stocks, each stocks's name, price, and stocks URI are added to the clipboard.

        :return: Each stock's name, price, and stocks URI
        :rtype: list[Union[str, NSURL]]

        .. versionadded:: 0.0.8
        """
        items = []
        names = self.name()
        prices = self.price()
        symbols = self.symbol()
        for index, name in enumerate(names):
            items.append(name + " - " + str(prices[index]))
            items.append(XABase.XAURL("stocks://?symbol=" + symbols[index]).xa_elem)

        return items

    def __repr__(self):
        return "<" + str(type(self)) + str(self.object_description()) + ">"


class XAStocksSavedStock(XABase.XAObject, XAClipboardCodable):
    """A class for interacting with stocks in Stocks.app.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the stock."""
        return self.xa_elem.properties()

    @property
    def name(self) -> str:
        """The name of the stock (The company name)."""
        reversed = self.xa_elem.objectDescription().get()[::-1]
        return reversed[reversed.index(",") + 1 :][::-1]

    @property
    def symbol(self) -> str:
        """The symbol for the stock."""
        return self.xa_elem.objectDescription().get().split(", ")[-1]

    @property
    def price(self) -> float:
        """The current price of the stock."""
        value = self.xa_elem.value().get()
        value = value.replace("selected, ", "")
        return float(value.split(", ")[0].replace(",", ""))

    @property
    def change(self) -> str:
        """The percentage or point change of the stock in the current trading session."""
        value = self.xa_elem.value().get()
        return value.split(", ")[-1]

    @property
    def selected(self) -> bool:
        """Whether the stock is the currently selected stock."""
        return self.xa_elem.selected().get()

    def show(self):
        """Shows the stock's tab in the front stock window.

        .. versionadded:: 0.0.6
        """
        self.xa_elem.actions()[0].perform()

    def get_clipboard_representation(self) -> list[Union[str, NSURL]]:
        """Gets a clipboard-codable representation of the stock.

        When the clipboard content is set to a saved stock, the stocks's name, price, and stocks URI are added to the clipboard.

        :return: The stock's name, price, and stocks URI
        :rtype: list[Union[str, NSURL]]

        .. versionadded:: 0.0.8
        """
        return [
            self.name + " - " + str(self.price),
            XABase.XAURL("stocks://?symbol=" + self.symbol).xa_elem,
        ]
