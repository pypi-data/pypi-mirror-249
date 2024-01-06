class CodeType:
    DIVISION = 'DIV'
    DISTRIBUTION_SITE = 'DSTS'
    DISTRIBUTION_TYPE = 'DSTT'
    NOTICE_TYPE = 'NOTI'
    NOTICE_PLATFORM = 'NP'
    OS_TYPE = 'OS'
    PRIORITY = 'PRI'

    @classmethod
    def get_display_name(cls, value) -> str:
        return {
            cls.DIVISION: "Division",
            cls.DISTRIBUTION_SITE: "Distribution Site",
            cls.DISTRIBUTION_TYPE: "Distribution Type",
            cls.NOTICE_TYPE: "Notice Type",
            cls.NOTICE_PLATFORM: "Notice Platform",
            cls.OS_TYPE: "Os Type",
            cls.PRIORITY: "Priority",
        }[value]
