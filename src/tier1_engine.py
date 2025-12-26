import datetime
import math
import pytz
import swisseph as swe
from kerykeion import AstrologicalSubject
from lunar_python import Solar, Lunar

class SolalendarTier1:
    """
    Solalendar Core Engine v4.1 (Feature Update)
    Added: Layer 2 'The Pinnacles' (Life Chapters)
    """

    def __init__(self, name, year, month, day, hour, minute, lat=35.6895, lng=139.6917, tz_str="Asia/Tokyo"):
        self.name = name
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.lat = lat
        self.lng = lng
        self.tz_str = tz_str
        
        # Datetime Setup
        local = pytz.timezone(tz_str)
        local_dt = local.localize(datetime.datetime(year, month, day, hour, minute))
        self.utc_dt = local_dt.astimezone(pytz.utc)
        self.current_year = datetime.datetime.now().year
        self.current_age = self.current_year - self.year
        
        # Layer 0: JDN Calculation
        self.jul_day_ut = swe.julday(year, month, day, hour + minute/60.0 - 9.0)

    # ---------------------------------------------------------
    # Helper: Numerology Reducer
    # ---------------------------------------------------------
    def _reduce(self, n):
        """Standard recursive reduction (11, 22, 33 preserved)"""
        while n > 9 and n not in [11, 22, 33]:
            n = sum(int(d) for d in str(n))
        return n
    
    def _reduce_single(self, n):
        """Force reduction to single digit (for Pinnacle calc base)"""
        while n > 9:
            n = sum(int(d) for d in str(n))
        return n

    # ---------------------------------------------------------
    # Layer 1: BIOS (Numerology)
    # ---------------------------------------------------------
    def _calculate_lpn(self):
        # Sum of Y+M+D
        total = self.year + self.month + self.day
        lpn = self._reduce(total)
        return lpn

    # ---------------------------------------------------------
    # Layer 2: Infra (Cycles & Pinnacles)
    # ---------------------------------------------------------
    def _get_infra_layer(self, lpn):
        # 1. Planetary Cycles (Saturn/Jupiter)
        saturn_cycle_count = int(self.current_age // 29.5) + 1
        jupiter_phase = self.current_age % 12
        
        # 2. The Pinnacles (Life Chapters)
        # Base numbers (Single digit reduction required for calculation)
        m_base = self._reduce_single(self.month)
        d_base = self._reduce_single(self.day)
        y_base = self._reduce_single(self.year)
        
        # Calculate 4 Pinnacles
        pin1 = self._reduce(m_base + d_base)
        pin2 = self._reduce(d_base + y_base)
        pin3 = self._reduce(pin1 + pin2)
        pin4 = self._reduce(m_base + y_base)
        
        # Calculate Timeline (Ages)
        # 1st Pinnacle ends at (36 - LPN)
        # If LPN is Master Number, reduce it for calculation (e.g. 11->2, 22->4)
        lpn_single = self._reduce_single(lpn)
        age_end_1 = 36 - lpn_single
        age_end_2 = age_end_1 + 9
        age_end_3 = age_end_2 + 9
        
        # Identify Current Stage
        current_pin = 0
        stage_name = ""
        if self.current_age <= age_end_1:
            current_pin = pin1
            stage_name = "1st Pinnacle (Formation)"
            range_str = f"Age 0 - {age_end_1}"
        elif self.current_age <= age_end_2:
            current_pin = pin2
            stage_name = "2nd Pinnacle (Production)"
            range_str = f"Age {age_end_1+1} - {age_end_2}"
        elif self.current_age <= age_end_3:
            current_pin = pin3
            stage_name = "3rd Pinnacle (Maturation)"
            range_str = f"Age {age_end_2+1} - {age_end_3}"
        else:
            current_pin = pin4
            stage_name = "4th Pinnacle (Integration)"
            range_str = f"Age {age_end_3+1}+"

        return {
            "saturn_cycle": f"Round {saturn_cycle_count}",
            "jupiter_phase": f"Year {jupiter_phase}/12",
            "pinnacle": {
                "current_number": current_pin,
                "current_stage": stage_name,
                "period_range": range_str,
                "all_pins": [pin1, pin2, pin3, pin4]
            }
        }

    # ---------------------------------------------------------
    # Layer 3 & 5: Env & Skin
    # ---------------------------------------------------------
    def _get_planetary_layers(self):
        subj = AstrologicalSubject(self.name, self.year, self.month, self.day, self.hour, self.minute, lat=self.lat, lng=self.lng, tz_str=self.tz_str, online=False)
        return {
            "Sun": {"sign": subj.sun.sign, "lon": subj.sun.position},
            "Moon": {"sign": subj.moon.sign, "lon": subj.moon.position},
            "Ascendant": subj.first_house.sign
        }

    # ---------------------------------------------------------
    # Layer 4: Runtime
    # ---------------------------------------------------------
    def _get_runtime_layer(self):
        solar = Solar.fromYmd(self.year, self.month, self.day)
        lunar = solar.getLunar()
        return {
            "eto_day": lunar.getDayInGanZhi(),
            "nayin": lunar.getDayNaYin(),
            "lunar_date": f"{lunar.getMonth()}月{lunar.getDay()}日"
        }

    # ---------------------------------------------------------
    # MAIN ANALYZE
    # ---------------------------------------------------------
    def analyze(self):
        lpn = self._calculate_lpn()
        infra = self._get_infra_layer(lpn)
        planets = self._get_planetary_layers()
        runtime = self._get_runtime_layer()
        
        return {
            "meta": {"version": "Solalendar Tier1 v4.1", "type": "PSC_Decode"},
            "layer_0_kernel": {
                "desc": "The Absolute",
                "jdn": self.jul_day_ut,
                "vector": f"{self.lat}, {self.lng}"
            },
            "layer_1_bios": {
                "desc": "Source Numerology",
                "lpn": lpn
            },
            "layer_2_infra": {
                "desc": "Social Cycles & Chapters",
                "cycles": infra
            },
            "layer_3_env": {
                "desc": "Display Environment",
                "sun_sign": planets["Sun"]["sign"]
            },
            "layer_4_runtime": {
                "desc": "System Clock",
                "moon_sign": planets["Moon"]["sign"],
                "eastern_root": runtime["eto_day"],
                "texture": runtime["nayin"]
            },
            "layer_5_skin": {
                "desc": "Interface",
                "ascendant": planets["Ascendant"]
            }
        }