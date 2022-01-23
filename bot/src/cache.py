from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional, Set, Tuple

from .data.db import execute_read_query

__all__ = ("cache",)

if TYPE_CHECKING:
    from _typings import (
        AccountData,
        AllianceAutoRoleData,
        AllianceData,
        AllianceSettingsData,
        CityData,
        ColorData,
        ConditionData,
        CredentialsData,
        EmbassyConfigData,
        EmbassyData,
        ForumData,
        GrantData,
        GuildSettingsData,
        GuildWelcomeSettingsData,
        MenuData,
        MenuInterfaceData,
        MenuItemData,
        NationData,
        RawColorData,
        RawTreasureData,
        RoleData,
        SubscriptionData,
        TargetData,
        TargetReminderData,
        TicketConfigData,
        TicketData,
        TradePriceData,
        TransactionData,
        TransactionRequestData,
        TreatyData,
        UserData,
    )

    from .data.classes import (
        Account,
        Alliance,
        AllianceAutoRole,
        AllianceSettings,
        City,
        Color,
        Condition,
        Credentials,
        Embassy,
        EmbassyConfig,
        Forum,
        Grant,
        GuildSettings,
        GuildWelcomeSettings,
        Menu,
        MenuInterface,
        MenuItem,
        Nation,
        Role,
        Subscription,
        Target,
        TargetReminder,
        Ticket,
        TicketConfig,
        TradePrices,
        Transaction,
        TransactionRequest,
        Treasure,
        Treaty,
        User,
    )


class Validate:
    def __init__(self) -> None:
        self.alliances: bool = False
        self.cities: bool = False
        self.colors: bool = False
        self.nations: bool = False
        self.prices: bool = False
        self.treasures: bool = False
        self.treaties: bool = False


class Cache:
    __slots__ = (
        "_accounts",
        "_alliances",
        "_alliance_auto_roles",
        "_alliance_settings",
        "_cities",
        "_colors",
        "_conditions",
        "_credentials",
        "_embassies",
        "_embassy_configs",
        "_forums",
        "_grants",
        "_guild_settings",
        "_guild_welcome_settings",
        "_users",
        "_menu_interfaces",
        "_menu_items",
        "_menus",
        "_nations",
        "_prices",
        "_roles",
        "_subscriptions",
        "_targets",
        "_target_reminders",
        "_ticket_configs",
        "_tickets",
        "_trades",
        "_transactions",
        "_transaction_requests",
        "_treasures",
        "_treaties",
        "_war_attacks",
        "_wars",
        "init",
        "validate",
    )

    def __init__(self):
        self._accounts: Dict[int, Account] = {}
        self._alliances: Dict[int, Alliance] = {}
        self._alliance_auto_roles: Set[AllianceAutoRole] = set()
        self._alliance_settings: Dict[int, AllianceSettings] = {}
        self._cities: Dict[int, City] = {}
        self._colors: Dict[str, Color] = {}
        self._conditions: Dict[int, Condition] = {}
        self._credentials: Dict[int, Credentials] = {}
        self._embassies: Dict[int, Embassy] = {}
        self._embassy_configs: Dict[int, EmbassyConfig] = {}
        self._forums: Dict[int, Forum] = {}
        self._grants: Dict[int, Grant] = {}
        self._guild_settings: Dict[int, GuildSettings] = {}
        self._guild_welcome_settings: Dict[int, GuildWelcomeSettings] = {}
        self._menu_interfaces: Set[MenuInterface] = set()
        self._menu_items: Dict[int, MenuItem] = {}
        self._menus: Dict[int, Menu] = {}
        self._nations: Dict[int, Nation] = {}
        self._prices: TradePrices
        self._roles: Dict[int, Role] = {}
        self._subscriptions: Dict[int, Subscription] = {}
        self._targets: Dict[int, Target] = {}
        self._target_reminders: Dict[int, TargetReminder] = {}
        self._ticket_configs: Dict[int, TicketConfig] = {}
        self._tickets: Dict[int, Ticket] = {}
        self._trades = {}  # NO CLASS YET
        self._transactions: Dict[int, Transaction] = {}
        self._transaction_requests: Dict[int, TransactionRequest] = {}
        self._treasures: List[Treasure] = []
        self._treaties: Set[Treaty] = set()
        self._users: Set[User] = set()
        self._war_attacks = {}  # NO CLASS YET
        self._wars = {}  # NO CLASS YET
        self.init: bool = False
        self.validate: Validate = Validate()

    async def initialize(self):  # sourcery no-metrics
        from .data.classes import (
            Account,
            Alliance,
            AllianceAutoRole,
            AllianceSettings,
            City,
            Color,
            Condition,
            Credentials,
            Embassy,
            EmbassyConfig,
            Forum,
            Grant,
            GuildSettings,
            GuildWelcomeSettings,
            Menu,
            MenuInterface,
            MenuItem,
            Nation,
            Role,
            Subscription,
            Target,
            TargetReminder,
            Ticket,
            TicketConfig,
            TradePrices,
            Transaction,
            TransactionRequest,
            Treasure,
            Treaty,
            User,
        )

        queries = [
            "SELECT * FROM accounts",
            "SELECT * FROM alliances;",
            "SELECT * FROM alliance_auto_roles;",
            "SELECT * FROM alliance_settings;",
            "SELECT * FROM cities;",
            "SELECT * FROM colors ORDER BY datetime DESC LIMIT 1;",
            "SELECT * FROM conditions;",
            "SELECT * FROM credentials;",
            "SELECT * FROM embassies;",
            "SELECT * FROM embassy_configs;",
            "SELECT * FROM forums;",
            "SELECT * FROM grants;",
            "SELECT * FROM guild_settings;",
            "SELECT * FROM guild_welcome_settings;",
            "SELECT * FROM menu_interfaces;",
            "SELECT * FROM menu_items;",
            "SELECT * FROM menus;",
            "SELECT * FROM nations;",
            "SELECT * FROM prices ORDER BY datetime DESC LIMIT 1;",
            "SELECT * FROM roles;",
            "SELECT * FROM subscriptions;",
            "SELECT * FROM targets;",
            "SELECT * FROM target_reminders;",
            "SELECT * FROM ticket_configs;",
            "SELECT * FROM tickets;",
            "SELECT * FROM transactions;",
            "SELECT * FROM transaction_requests;",
            "SELECT * FROM treasures ORDER BY datetime DESC LIMIT 1;",
            "SELECT * FROM treaties;",
            "SELECT * FROM users;",
        ]
        data: Tuple[  # type: ignore
            List[AccountData],
            List[AllianceData],
            List[AllianceAutoRoleData],
            List[AllianceSettingsData],
            List[CityData],
            List[RawColorData],
            List[ConditionData],
            List[CredentialsData],
            List[EmbassyData],
            List[EmbassyConfigData],
            List[ForumData],
            List[GrantData],
            List[GuildSettingsData],
            List[GuildWelcomeSettingsData],
            List[MenuInterfaceData],
            List[MenuItemData],
            List[MenuData],
            List[NationData],
            List[TradePriceData],
            List[RoleData],
            List[SubscriptionData],
            List[TargetData],
            List[TargetReminderData],
            List[TicketConfigData],
            List[TicketData],
            List[TransactionData],
            List[TransactionRequestData],
            List[RawTreasureData],
            List[TreatyData],
            List[UserData],
        ] = tuple(  # type: ignore
            await asyncio.gather(*(execute_read_query(query) for query in queries))  # type: ignore
        )
        (
            accounts,
            alliances,
            alliance_auto_roles,
            alliance_settings,
            cities,
            colors,
            conditions,
            credentials,
            embassies,
            embassy_configs,
            forums,
            grants,
            guild_settings,
            guild_welcome_settings,
            menu_interfaces,
            menu_items,
            menus,
            nations,
            prices,
            roles,
            subscriptions,
            targets,
            target_reminders,
            ticket_configs,
            tickets,
            transactions,
            transaction_requests,
            treasures,
            treaties,
            users,
        ) = data
        for i in accounts:
            i = Account(i)
            self._accounts[i.id] = i
        for i in alliances:
            i = Alliance(i)
            self._alliances[i.id] = i
        for i in alliance_auto_roles:
            i = AllianceAutoRole(i)
            self._alliance_auto_roles.add(i)
        for i in alliance_settings:
            i = AllianceSettings(i)
            self._alliance_settings[i.alliance_id] = i
        for i in cities:
            i = City(i)
            self._cities[i.id] = i
        for i in colors[0]["colors"]:
            i = Color(i)
            self._colors[i.color] = i
        for i in conditions:
            i = Condition(i)
            self._conditions[i.id] = i
        for i in credentials:
            i = Credentials(i)
            self._credentials[i.nation_id] = i
        for i in embassies:
            i = Embassy(i)
            self._embassies[i.id] = i
        for i in embassy_configs:
            i = EmbassyConfig(i)
            self._embassy_configs[i.id] = i
        for i in forums:
            i = Forum(i)
            self._forums[i.id] = i
        for i in grants:
            i = Grant(i)
            self._grants[i.id] = i
        for i in guild_settings:
            i = GuildSettings(i)
            self._guild_settings[i.guild_id] = i
        for i in guild_welcome_settings:
            i = GuildWelcomeSettings(i)
            self._guild_welcome_settings[i.guild_id] = i
        for i in menu_interfaces:
            i = MenuInterface(i)
            self._menu_interfaces.add(i)
        for i in menu_items:
            i = MenuItem(i)
            self._menu_items[i.id] = i
        for i in menus:
            i = Menu(i)
            self._menus[i.id] = i
        for i in nations:
            i = Nation(i)
            self._nations[i.id] = i
        # for some reason is the only JSON type to give string, so did compatible with proper loading fix here
        self._prices = TradePrices(
            {  # type: ignore
                key: json.loads(value)
                if key != "datetime" and isinstance(value, str)
                else value
                for key, value in dict(prices[0]).items()
            }
        )
        for i in roles:
            i = Role(i)
            self._roles[i.id] = i
        for i in subscriptions:
            i = Subscription(i)
            self._subscriptions[i.id] = i
        for i in targets:
            i = Target(i)
            self._targets[i.id] = i
        for i in target_reminders:
            i = TargetReminder(i)
            self._target_reminders[i.id] = i
        for i in ticket_configs:
            i = TicketConfig(i)
            self._ticket_configs[i.id] = i
        for i in tickets:
            i = Ticket(i)
            self._tickets[i.id] = i
        for i in transactions:
            i = Transaction(i)
            self._transactions[i.id] = i
        for i in transaction_requests:
            i = TransactionRequest(i)
            self._transaction_requests[i.id] = i
        for i in (  # type
            json.loads(treasures[0]["treasures"])
            if isinstance(treasures[0]["treasures"], str)
            else treasures[0]["treasures"]
        ):
            i = Treasure(i)
            self._treasures.append(i)
        for i in treaties:
            i = Treaty(
                i,
                {
                    i["from_"]: self.get_alliance(i["from_"]),  # type: ignore
                    i["to_"]: self.get_alliance(i["to_"]),  # type: ignore
                },
            )
            if i.stopped is None:
                self._treaties.add(i)
        for i in users:
            i = User(i)
            self._users.add(i)
        self.init = True

    @property
    def accounts(self) -> Set[Account]:
        return set(self._accounts.values())

    @property
    def alliances(self) -> Set[Alliance]:
        return set(self._alliances.values())

    @property
    def alliance_auto_roles(self) -> Set[AllianceAutoRole]:
        return self._alliance_auto_roles

    @property
    def cities(self) -> Set[City]:
        return set(self._cities.values())

    @property
    def colors(self) -> Set[Color]:
        return set(self._colors.values())

    @property
    def conditions(self) -> Set[Condition]:
        return set(self._conditions.values())

    @property
    def credentials(self) -> Set[Credentials]:
        return set(self._credentials.values())

    @property
    def embassies(self) -> Set[Embassy]:
        return set(self._embassies.values())

    @property
    def embassy_configs(self) -> Set[EmbassyConfig]:
        return set(self._embassy_configs.values())

    @property
    def forums(self) -> Set[Forum]:
        return set(self._forums.values())

    @property
    def guild_settings(self) -> Set[GuildSettings]:
        return set(self._guild_settings.values())

    @property
    def guild_welcome_settings(self) -> Set[GuildWelcomeSettings]:
        return set(self._guild_welcome_settings.values())

    @property
    def menu_interfaces(self) -> Set[MenuInterface]:
        return self._menu_interfaces

    @property
    def menu_items(self) -> Set[MenuItem]:
        return set(self._menu_items.values())

    @property
    def menus(self) -> Set[Menu]:
        return set(self._menus.values())

    @property
    def nations(self) -> Set[Nation]:
        return set(self._nations.values())

    @property
    def prices(self) -> TradePrices:
        return self._prices

    @property
    def roles(self) -> Set[Role]:
        return set(self._roles.values())

    @property
    def subscriptions(self) -> Set[Subscription]:
        return set(self._subscriptions.values())

    @property
    def targets(self) -> Set[Target]:
        return set(self._targets.values())

    @property
    def target_reminders(self) -> Set[TargetReminder]:
        return set(self._target_reminders.values())

    @property
    def ticket_configs(self) -> Set[TicketConfig]:
        return set(self._ticket_configs.values())

    @property
    def tickets(self) -> Set[Ticket]:
        return set(self._tickets.values())

    @property
    def transactions(self) -> Set[Transaction]:
        return set(self._transactions.values())

    @property
    def transaction_requests(self) -> Set[TransactionRequest]:
        return set(self._transaction_requests.values())

    @property
    def treasures(self) -> List[Treasure]:
        return self._treasures

    @property
    def treaties(self) -> Set[Treaty]:
        return self._treaties

    @property
    def users(self) -> Set[User]:
        return self._users

    def hook_alliance(
        self, action: Literal["update", "create", "delete"], data: AllianceData
    ) -> None:
        from .data.classes import Alliance

        if action == "delete":
            i = self._alliances.get(data["id"])
            if i:
                del i
            return
        try:
            self._alliances[data["id"]].update(data)
        except KeyError:
            self._alliances[data["id"]] = Alliance(data)

    def hook_city(
        self, action: Literal["update", "create", "delete"], data: CityData
    ) -> None:
        from .data.classes import City

        if action == "delete":
            i = self._cities.get(data["id"])
            if i:
                del i
            return
        try:
            self._cities[data["id"]].update(data)
        except KeyError:
            self._cities[data["id"]] = City(data)

    def hook_color(self, action: Literal["update"], data: ColorData) -> None:
        from .data.classes import Color

        try:
            self._colors[data["color"]].update(data)
        except KeyError:
            self._colors[data["color"]] = Color(data)

    def hook_nation(
        self, action: Literal["update", "create", "delete"], data: NationData
    ) -> None:
        from .data.classes import Nation

        if action == "delete":
            i = self._nations.get(data["id"])
            if i:
                del i
            return
        try:
            self._nations[data["id"]].update(data)
        except KeyError:
            self._nations[data["id"]] = Nation(data)

    def hook_price(self, action: Literal["update"], data: TradePriceData) -> None:
        try:
            self._prices.update(data)
        except KeyError:
            self._prices.update(data)

    def hook_treasure(self, action: Literal["update"], data: Dict[Any, Any]) -> None:
        for new in data.values():
            next(i.update(new) for i in self._treasures if i.name == new["name"])

    def hook_treaty(
        self, action: Literal["create", "update", "delete"], data: TreatyData
    ) -> None:
        from .data.classes import Treaty

        alliances: Dict[int, Alliance] = {  # type: ignore
            data["from_"]: self.get_alliance(data["from_"]),
            data["to_"]: self.get_alliance(data["to_"]),
        }
        if action == "delete":
            treaty = next(
                i
                for i in self._treaties
                if (i.from_ and i.from_.id) == data["from_"]
                or (i.to_ and i.to_.id) == data["to_"]
            )
            treaty.update(data, alliances)
        self._treaties.add(Treaty(data, alliances))

    def get_account(self, id: int, /) -> Optional[Account]:
        return self._accounts.get(id)

    def get_alliance(self, id: int, /) -> Optional[Alliance]:
        return self._alliances.get(id)

    def get_alliance_settings(self, id: int, /) -> Optional[AllianceSettings]:
        return self._alliance_settings.get(id)

    def get_city(self, id: int, /) -> Optional[City]:
        return self._cities.get(id)

    def get_color(self, name: str, /) -> Optional[Color]:
        return self._colors.get(name)

    def get_condition(self, id: int, /) -> Optional[Condition]:
        return self._conditions.get(id)

    def get_credentials(self, id: int, /) -> Optional[Credentials]:
        return self._credentials.get(id)

    def get_embassy(self, id: int, /) -> Optional[Embassy]:
        return self._embassies.get(id)

    def get_embassy_config(self, id: int, /) -> Optional[EmbassyConfig]:
        return self._embassy_configs.get(id)

    def get_forum(self, id: int, /) -> Optional[Forum]:
        return self._forums.get(id)

    def get_grant(self, id: int, /) -> Optional[Grant]:
        return self._grants.get(id)

    def get_guild_settings(self, id: int, /) -> Optional[GuildSettings]:
        return self._guild_settings.get(id)

    def get_guild_welcome_settings(self, id: int, /) -> Optional[GuildWelcomeSettings]:
        return self._guild_welcome_settings.get(id)

    def get_menu_interface(
        self, menu_id: int, message_id: int, /
    ) -> Optional[MenuInterface]:
        try:
            return next(
                i
                for i in self._menu_interfaces
                if i.menu_id == menu_id and i.message_id == message_id
            )
        except StopIteration:
            return

    def get_menu_item(self, id: int, /) -> Optional[MenuItem]:
        return self._menu_items.get(id)

    def get_menu(self, id: int, /) -> Optional[Menu]:
        return self._menus.get(id)

    def get_nation(self, id: int, /) -> Optional[Nation]:
        return self._nations.get(id)

    def get_prices(self) -> Optional[TradePrices]:
        return self._prices

    def get_role(self, id: int, /) -> Optional[Role]:
        return self._roles.get(id)

    def get_subscription(self, id: int, /) -> Optional[Subscription]:
        return self._subscriptions.get(id)

    def get_target(self, id: int, /) -> Optional[Target]:
        return self._targets.get(id)

    def get_target_reminder(self, id: int, /) -> Optional[TargetReminder]:
        return self._target_reminders.get(id)

    def get_ticket_config(self, id: int, /) -> Optional[TicketConfig]:
        return self._ticket_configs.get(id)

    def get_ticket(self, id: int, /) -> Optional[Ticket]:
        return self._tickets.get(id)

    def get_transaction(self, id: int, /) -> Optional[Transaction]:
        return self._transactions.get(id)

    def get_transaction_request(self, id: int, /) -> Optional[TransactionRequest]:
        return self._transaction_requests.get(id)

    def get_treasure(self, name: str, /) -> Optional[Treasure]:
        try:
            return next(i for i in self._treasures if i.name == name)
        except StopIteration:
            return

    def get_treaty(self, from_: int, to_: int, treaty_type: str, /) -> Optional[Treaty]:
        try:
            return next(
                i
                for i in self._treaties
                if i.from_id == from_
                and i.to_id == to_
                and i.treaty_type == treaty_type
            )
        except StopIteration:
            return

    def get_user(self, id: int, /) -> Optional[User]:
        try:
            return next(i for i in self._users if i.user_id == id or i.nation_id == id)
        except StopIteration:
            return

    def add_account(self, account: Account) -> None:
        self._accounts[account.id] = account

    def add_alliance_auto_role(self, role: AllianceAutoRole, /) -> None:
        self._alliance_auto_roles.add(role)

    def add_alliance_settings(self, settings: AllianceSettings, /) -> None:
        self._alliance_settings[settings.alliance_id] = settings

    def add_condition(self, condition: Condition, /) -> None:
        self._conditions[condition.id] = condition

    def add_credentials(self, credentials: Credentials, /) -> None:
        self._credentials[credentials.nation_id] = credentials

    def add_embassy(self, embassy: Embassy, /) -> None:
        self._embassies[embassy.id] = embassy

    def add_embassy_config(self, config: EmbassyConfig, /) -> None:
        self._embassy_configs[config.id] = config

    def add_grant(self, grant: Grant, /) -> None:
        self._grants[grant.id] = grant

    def add_guild_settings(self, settings: GuildSettings, /) -> None:
        self._guild_settings[settings.guild_id] = settings

    def add_guild_welcome_settings(self, settings: GuildWelcomeSettings, /) -> None:
        self._guild_welcome_settings[settings.guild_id] = settings

    def add_menu(self, menu: Menu, /) -> None:
        self._menus[menu.id] = menu

    def add_menu_interface(self, interface: MenuInterface, /) -> None:
        self._menu_interfaces.add(interface)

    def add_menu_item(self, item: MenuItem, /) -> None:
        self._menu_items[item.id] = item

    def add_role(self, role: Role, /) -> None:
        self._roles[role.id] = role

    def add_subscription(self, subscription: Subscription, /) -> None:
        self._subscriptions[subscription.id] = subscription

    def add_ticket(self, ticket: Ticket, /) -> None:
        self._tickets[ticket.id] = ticket

    def add_ticket_config(self, config: TicketConfig, /) -> None:
        self._ticket_configs[config.id] = config

    def add_target(self, target: Target, /) -> None:
        self._targets[target.id] = target

    def add_target_reminder(self, reminder: TargetReminder, /) -> None:
        self._target_reminders[reminder.id] = reminder

    def add_transaction(self, transaction: Transaction, /) -> None:
        self._transactions[transaction.id] = transaction

    def add_transaction_request(self, request: TransactionRequest, /) -> None:
        self._transaction_requests[request.id] = request

    def add_user(self, user: User, /) -> None:
        self._users.add(user)

    def remove_account(self, account: Account, /) -> None:
        self._accounts.pop(account.id)

    def remove_alliance_auto_role(self, role: AllianceAutoRole, /) -> None:
        self._alliance_auto_roles.remove(role)

    def remove_condition(self, condition: Condition, /) -> None:
        self._conditions.pop(condition.id)

    def remove_credentials(self, credentials: Credentials, /) -> None:
        self._credentials.pop(credentials.nation_id)

    def remove_embassy(self, embassy: Embassy, /) -> None:
        self._embassies.pop(embassy.id)

    def remove_menu_interface(self, message_id: int, /) -> None:
        for i in self.menu_interfaces:
            if i.message_id == message_id:
                self._menu_interfaces.remove(i)
                break

    def remove_role(self, role: Role, /) -> None:
        self._roles.pop(role.id)

    def remove_subscription(self, subscription: Subscription, /) -> None:
        self._subscriptions.pop(subscription.id)

    def remove_target_reminder(self, reminder: TargetReminder, /) -> None:
        self._target_reminders.pop(reminder.id)

    def remove_transaction(self, transaction: Transaction, /) -> None:
        self._transactions.pop(transaction.id)

    def remove_transaction_request(self, request: TransactionRequest, /) -> None:
        self._transaction_requests.pop(request.id)

    def remove_user(self, user: User, /) -> None:
        self._users.remove(user)


cache = Cache()