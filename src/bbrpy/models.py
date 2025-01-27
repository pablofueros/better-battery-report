from datetime import datetime

from pydantic_xml import BaseXmlModel, attr, element, wrapped

from .generator import generate_battery_report_xml

NSMAP = {"": "http://schemas.microsoft.com/battery/2012"}


class ReportInformation(BaseXmlModel, nsmap=NSMAP):
    ReportGuid: str = element()
    ReportVersion: str = element()
    ScanTime: datetime = element()
    LocalScanTime: datetime = element()
    ReportStartTime: datetime = element()
    LocalReportStartTime: datetime = element()
    ReportDuration: int = element()
    UtcOffset: str = element()


class SystemInformation(BaseXmlModel, nsmap=NSMAP):
    ComputerName: str = element()
    SystemManufacturer: str = element()
    SystemProductName: str = element()
    BIOSDate: str = element()
    BIOSVersion: str = element()
    OSBuild: str = element()
    PlatformRole: str = element()
    ConnectedStandby: int = element()


class Battery(BaseXmlModel, nsmap=NSMAP):
    Id: str = element()
    Manufacturer: str = element()
    SerialNumber: str = element()
    ManufactureDate: str | None = element(default=None)
    Chemistry: str = element()
    LongTerm: int = element()
    RelativeCapacity: int = element()
    DesignCapacity: int = element()
    FullChargeCapacity: int = element()
    CycleCount: int = element()


class DesignCapacity(BaseXmlModel, nsmap=NSMAP):
    Capacity: int = element()
    ActiveRuntime: str = element()
    ConnectedStandbyRuntime: str = element()


class FullChargeCapacity(BaseXmlModel, nsmap=NSMAP):
    Capacity: int = element()
    ActiveRuntime: str = element()
    ConnectedStandbyRuntime: str = element()


class RuntimeEstimates(BaseXmlModel, nsmap=NSMAP):
    DesignCapacity: DesignCapacity
    FullChargeCapacity: FullChargeCapacity


class UsageEntry(BaseXmlModel, nsmap=NSMAP):
    Timestamp: datetime = attr()
    LocalTimestamp: datetime = attr()
    Duration: int = attr()
    Ac: int = attr()
    EntryType: str = attr()
    ChargeCapacity: int = attr()
    Discharge: int = attr()
    FullChargeCapacity: int = attr()
    IsNextOnBattery: int = attr()


class HistoryEntry(BaseXmlModel, nsmap=NSMAP):
    StartDate: datetime = attr()
    LocalStartDate: datetime = attr()
    EndDate: datetime = attr()
    LocalEndDate: datetime = attr()
    DesignCapacity: int = attr()
    FullChargeCapacity: int = attr()
    CycleCount: int = attr()
    ActiveAcTime: str = attr()
    ActiveDcTime: str = attr()
    CsAcTime: str = attr()
    CsDcTime: str = attr()
    ActiveDcEnergy: int = attr()
    CsDcEnergy: int = attr()
    EstimatedDesignActiveTime: str = attr()
    EstimatedFullChargeActiveTime: str = attr()
    EstimatedDesignCsTime: str = attr()
    EstimatedFullChargeCsTime: str = attr()
    BatteryChanged: int = attr()


class Drain(BaseXmlModel, nsmap=NSMAP):
    StartTimestamp: datetime = attr()
    LocalStartTimestamp: datetime = attr()
    EndTimestamp: datetime = attr()
    LocalEndTimestamp: datetime = attr()
    StartChargeCapacity: int = attr()
    StartFullChargeCapacity: int = attr()
    EndChargeCapacity: int = attr()
    EndFullChargeCapacity: int = attr()


class BatteryReport(BaseXmlModel, nsmap=NSMAP):
    ReportInformation: ReportInformation
    SystemInformation: SystemInformation
    Batteries: list[Battery] = wrapped("Batteries", element("Battery"))
    RuntimeEstimates: RuntimeEstimates
    RecentUsage: list[UsageEntry] = wrapped("RecentUsage", element("UsageEntry"))
    History: list[HistoryEntry] = wrapped("History", element("HistoryEntry"))
    EnergyDrains: list[Drain] = wrapped("EnergyDrains", element("Drain"))

    @classmethod
    def generate(cls) -> "BatteryReport":
        """Generate a new battery report from the system."""
        xml_report = generate_battery_report_xml()
        return cls.from_xml(xml_report)

    @property
    def computer_name(self):
        return self.SystemInformation.ComputerName

    @property
    def scan_time(self):
        return self.ReportInformation.LocalScanTime

    @property
    def design_cap(self):
        return self.RuntimeEstimates.DesignCapacity.Capacity

    @property
    def full_cap(self):
        return self.RuntimeEstimates.FullChargeCapacity.Capacity
