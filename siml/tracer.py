from colorama import Fore, Style, init
init(autoreset=True)

class Tracer: 
    enabled = False

    def __init__(self, section: str | None = None):
        self.section = section

    def info(self, message: str):
        if not self.enabled:
            return
        
        label = Fore.CYAN + "[INFO]" + Style.RESET_ALL
        section = f"{Fore.WHITE}[{self.section}]{Style.RESET_ALL} " if self.section else ""
        print(f"\n{label} {section} {message}")

    def debug(self, message: str):
        if not self.enabled:
            return
        
        label = Fore.YELLOW + "[DEBUG]" + Style.RESET_ALL
        section = f"{Fore.WHITE}[{self.section}]{Style.RESET_ALL} " if self.section else ""
        print(f"\n{label} {section} {message}")

    def warn(self, message: str):
        if not self.enabled:
            return
        
        label = Fore.MAGENTA + "[WARNING]" + Style.RESET_ALL
        section = f"{Fore.WHITE}[{self.section}]{Style.RESET_ALL} " if self.section else ""
        print(f"\n{label} {section} {message}")

    def failure(self, message: str):
        if not self.enabled:
            return
        
        label = Fore.RED + "[FAILURE]" + Style.RESET_ALL
        section = f"{Fore.WHITE}[{self.section}]{Style.RESET_ALL} " if self.section else ""
        print(f"\n{label} {section} {message}")

    
        
