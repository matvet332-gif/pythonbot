def create_safe_globals(self):
    """Создание безопасного глобального контекста"""
    safe_globals = {}
    
    # Базовые встроенные функции
    safe_builtins = {}
    for func in self.whitelisted_builtins:
        if func in __builtins__:
            safe_builtins[func] = __builtins__[func]
    
    safe_globals['__builtins__'] = safe_builtins
    
    # Математические функции
    try:
        import math
        safe_math = {
            'sqrt', 'pow', 'sin', 'cos', 'tan', 'log', 'log10', 
            'pi', 'e', 'ceil', 'floor', 'fabs', 'factorial',
            'degrees', 'radians', 'acos', 'asin', 'atan'
        }
        
        safe_globals['math'] = {
            func: getattr(math, func) 
            for func in safe_math 
            if hasattr(math, func)
        }
    except ImportError:
        pass
    
    # Добавляем безопасный print
    safe_globals['print'] = print
    
    return safe_globals
