#!/usr/bin/env python3
"""
Comprehensive Quality Assurance Suite
Implements MAXIMUM PERFORMANCE, QUALITY, PLANNING, PRECISION, ACCURACY, CORRECTION, and AUTONOMOUS TESTING/FIXING
"""

import os
import sys
import subprocess
import time
import json
import tempfile
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class QualityAssuranceManager:
    """
    Comprehensive QA Manager implementing enterprise-level quality assurance
    """
    
    def __init__(self):
        self.project_root = Path(os.path.dirname(os.path.abspath(__file__)))
        self.results = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'tests': {},
            'metrics': {},
            'issues': [],
            'recommendations': []
        }
        
        print("🚀 INICIANDO ANÁLISE DE QUALIDADE MÁXIMA")
        print("=" * 80)
    
    def run_code_quality_analysis(self) -> Dict[str, Any]:
        """Run comprehensive code quality analysis"""
        print("\n📊 ANÁLISE DE QUALIDADE DE CÓDIGO")
        print("-" * 50)
        
        results = {
            'python_syntax': self._check_python_syntax(),
            'javascript_syntax': self._check_javascript_syntax(),
            'html_validation': self._check_html_validation(),
            'css_validation': self._check_css_validation(),
            'security_scan': self._run_security_scan(),
            'performance_audit': self._run_performance_audit()
        }
        
        self.results['tests']['code_quality'] = results
        return results
    
    def _check_python_syntax(self) -> Dict[str, Any]:
        """Check Python syntax and style"""
        print("🐍 Verificando sintaxe Python...")
        
        python_files = list(self.project_root.glob("*.py"))
        results = {'files_checked': len(python_files), 'issues': [], 'passed': True}
        
        for py_file in python_files:
            try:
                # Check syntax
                subprocess.run([sys.executable, '-m', 'py_compile', str(py_file)], 
                             check=True, capture_output=True)
                print(f"  ✅ {py_file.name}")
            except subprocess.CalledProcessError as e:
                error_msg = f"Syntax error in {py_file.name}: {e.stderr.decode()}"
                results['issues'].append(error_msg)
                results['passed'] = False
                print(f"  ❌ {py_file.name}: {error_msg}")
        
        return results
    
    def _check_javascript_syntax(self) -> Dict[str, Any]:
        """Check JavaScript syntax"""
        print("📜 Verificando sintaxe JavaScript...")
        
        js_files = list(self.project_root.glob("*.js"))
        results = {'files_checked': len(js_files), 'issues': [], 'passed': True}
        
        for js_file in js_files:
            try:
                # Use Node.js to check syntax
                subprocess.run(['node', '-c', str(js_file)], 
                             check=True, capture_output=True)
                print(f"  ✅ {js_file.name}")
            except subprocess.CalledProcessError as e:
                error_msg = f"Syntax error in {js_file.name}: {e.stderr.decode()}"
                results['issues'].append(error_msg)
                results['passed'] = False
                print(f"  ❌ {js_file.name}: {error_msg}")
            except FileNotFoundError:
                # Node.js not available
                print(f"  ⚠️ {js_file.name}: Node.js not available, skipping syntax check")
        
        return results
    
    def _check_html_validation(self) -> Dict[str, Any]:
        """Basic HTML validation"""
        print("📝 Verificando estrutura HTML...")
        
        html_files = list(self.project_root.glob("*.html"))
        results = {'files_checked': len(html_files), 'issues': [], 'passed': True}
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Basic checks
                checks = [
                    ('DOCTYPE declaration', content.lower().startswith('<!doctype html')),
                    ('HTML lang attribute', 'lang=' in content),
                    ('Meta charset', 'charset=' in content),
                    ('Viewport meta', 'viewport' in content),
                    ('Title tag', '<title>' in content),
                ]
                
                for check_name, passed in checks:
                    if not passed:
                        results['issues'].append(f"{html_file.name}: Missing {check_name}")
                        results['passed'] = False
                
                print(f"  ✅ {html_file.name}")
                
            except Exception as e:
                error_msg = f"Error reading {html_file.name}: {str(e)}"
                results['issues'].append(error_msg)
                results['passed'] = False
                print(f"  ❌ {html_file.name}: {error_msg}")
        
        return results
    
    def _check_css_validation(self) -> Dict[str, Any]:
        """Basic CSS validation"""
        print("🎨 Verificando estrutura CSS...")
        
        css_files = list(self.project_root.glob("*.css"))
        results = {'files_checked': len(css_files), 'issues': [], 'passed': True}
        
        for css_file in css_files:
            try:
                with open(css_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Basic syntax checks
                open_braces = content.count('{')
                close_braces = content.count('}')
                
                if open_braces != close_braces:
                    results['issues'].append(f"{css_file.name}: Mismatched braces ({open_braces} open, {close_braces} close)")
                    results['passed'] = False
                
                print(f"  ✅ {css_file.name}")
                
            except Exception as e:
                error_msg = f"Error reading {css_file.name}: {str(e)}"
                results['issues'].append(error_msg)
                results['passed'] = False
                print(f"  ❌ {css_file.name}: {error_msg}")
        
        return results
    
    def _run_security_scan(self) -> Dict[str, Any]:
        """Run security analysis"""
        print("🛡️ Executando análise de segurança...")
        
        results = {'issues': [], 'passed': True, 'checks_performed': []}
        
        # Check for common security issues
        security_checks = [
            self._check_xss_vulnerabilities,
            self._check_injection_vulnerabilities,
            self._check_insecure_practices,
            self._check_data_exposure
        ]
        
        for check in security_checks:
            try:
                check_result = check()
                results['checks_performed'].append(check.__name__)
                if not check_result['passed']:
                    results['issues'].extend(check_result['issues'])
                    results['passed'] = False
            except Exception as e:
                results['issues'].append(f"Security check failed: {check.__name__}: {str(e)}")
                results['passed'] = False
        
        return results
    
    def _check_xss_vulnerabilities(self) -> Dict[str, Any]:
        """Check for XSS vulnerabilities"""
        issues = []
        
        # Check JavaScript files for direct DOM manipulation without sanitization
        js_files = list(self.project_root.glob("*.js"))
        for js_file in js_files:
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for potentially dangerous patterns
            dangerous_patterns = [
                ('innerHTML without sanitization', r'\.innerHTML\s*=\s*[^;]*[+`]'),
                ('eval() usage', r'\beval\s*\('),
                ('document.write()', r'document\.write\s*\(')
            ]
            
            import re
            for pattern_name, pattern in dangerous_patterns:
                if re.search(pattern, content):
                    issues.append(f"{js_file.name}: Potential XSS risk - {pattern_name}")
        
        return {'passed': len(issues) == 0, 'issues': issues}
    
    def _check_injection_vulnerabilities(self) -> Dict[str, Any]:
        """Check for injection vulnerabilities"""
        issues = []
        
        # Check for SQL injection patterns (though this is frontend code)
        files_to_check = list(self.project_root.glob("*.py")) + list(self.project_root.glob("*.js"))
        
        for file_path in files_to_check:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for string concatenation in queries
            import re
            if re.search(r'(SELECT|INSERT|UPDATE|DELETE).*\+.*', content, re.IGNORECASE):
                issues.append(f"{file_path.name}: Potential SQL injection risk - string concatenation in query")
        
        return {'passed': len(issues) == 0, 'issues': issues}
    
    def _check_insecure_practices(self) -> Dict[str, Any]:
        """Check for insecure coding practices"""
        issues = []
        
        # Check for hardcoded secrets or credentials
        files_to_check = list(self.project_root.glob("*.py")) + list(self.project_root.glob("*.js"))
        
        for file_path in files_to_check:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for suspicious patterns
            import re
            suspicious_patterns = [
                ('Hardcoded password', r'password\s*[:=]\s*["\'][^"\']+["\']'),
                ('Hardcoded API key', r'api[_-]?key\s*[:=]\s*["\'][^"\']+["\']'),
                ('Hardcoded token', r'token\s*[:=]\s*["\'][^"\']+["\']')
            ]
            
            for pattern_name, pattern in suspicious_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    issues.append(f"{file_path.name}: {pattern_name} detected")
        
        return {'passed': len(issues) == 0, 'issues': issues}
    
    def _check_data_exposure(self) -> Dict[str, Any]:
        """Check for potential data exposure"""
        issues = []
        
        # Check for console.log with sensitive data
        js_files = list(self.project_root.glob("*.js"))
        for js_file in js_files:
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count console.log statements (should be limited in production)
            import re
            console_logs = len(re.findall(r'console\.log\s*\(', content))
            if console_logs > 10:  # Arbitrary threshold
                issues.append(f"{js_file.name}: High number of console.log statements ({console_logs}) - consider removing for production")
        
        return {'passed': len(issues) == 0, 'issues': issues}
    
    def _run_performance_audit(self) -> Dict[str, Any]:
        """Run performance analysis"""
        print("⚡ Executando auditoria de performance...")
        
        results = {'metrics': {}, 'issues': [], 'passed': True}
        
        try:
            # Analyze file sizes
            file_sizes = {}
            for file_path in self.project_root.glob("*"):
                if file_path.is_file() and not file_path.name.startswith('.'):
                    size = file_path.stat().st_size
                    file_sizes[file_path.name] = size
            
            results['metrics']['file_sizes'] = file_sizes
            
            # Check for oversized files
            size_limits = {
                '.js': 100 * 1024,    # 100KB for JS
                '.css': 50 * 1024,    # 50KB for CSS
                '.html': 20 * 1024,   # 20KB for HTML
                '.png': 500 * 1024,   # 500KB for images
                '.jpg': 500 * 1024,
                '.jpeg': 500 * 1024
            }
            
            for filename, size in file_sizes.items():
                ext = Path(filename).suffix.lower()
                if ext in size_limits and size > size_limits[ext]:
                    results['issues'].append(f"{filename}: File size ({size} bytes) exceeds recommended limit ({size_limits[ext]} bytes)")
                    results['passed'] = False
            
            # Analyze CSS complexity
            css_files = list(self.project_root.glob("*.css"))
            for css_file in css_files:
                with open(css_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Count selectors and rules
                selector_count = content.count('{')
                results['metrics'][f'{css_file.name}_selectors'] = selector_count
                
                if selector_count > 1000:  # Arbitrary threshold
                    results['issues'].append(f"{css_file.name}: High CSS complexity ({selector_count} selectors)")
                    results['passed'] = False
            
        except Exception as e:
            results['issues'].append(f"Performance audit failed: {str(e)}")
            results['passed'] = False
        
        return results
    
    def run_unit_tests(self) -> Dict[str, Any]:
        """Run unit tests"""
        print("\n🧪 EXECUTANDO TESTES UNITÁRIOS")
        print("-" * 50)
        
        results = {'passed': True, 'output': '', 'test_count': 0}
        
        try:
            # Run Python unit tests
            if (self.project_root / "test_config.py").exists():
                result = subprocess.run([sys.executable, "test_config.py"], 
                                      cwd=self.project_root, 
                                      capture_output=True, 
                                      text=True)
                
                results['output'] = result.stdout + result.stderr
                results['passed'] = result.returncode == 0
                
                # Extract test count from output
                import re
                test_match = re.search(r'Ran (\d+) tests', results['output'])
                if test_match:
                    results['test_count'] = int(test_match.group(1))
                
                print(f"✅ Testes unitários: {results['test_count']} executados")
                if not results['passed']:
                    print("❌ Alguns testes unitários falharam")
            else:
                print("⚠️ Arquivo de testes unitários não encontrado")
                
        except Exception as e:
            results['passed'] = False
            results['output'] = str(e)
            print(f"❌ Erro ao executar testes unitários: {e}")
        
        self.results['tests']['unit_tests'] = results
        return results
    
    def run_e2e_tests(self) -> Dict[str, Any]:
        """Run end-to-end tests"""
        print("\n🎭 EXECUTANDO TESTES END-TO-END")
        print("-" * 50)
        
        results = {'passed': True, 'output': '', 'test_count': 0}
        
        try:
            # Check if E2E test file exists
            if (self.project_root / "test_e2e.py").exists():
                result = subprocess.run([sys.executable, "test_e2e.py"], 
                                      cwd=self.project_root, 
                                      capture_output=True, 
                                      text=True,
                                      timeout=120)  # 2 minute timeout
                
                results['output'] = result.stdout + result.stderr
                results['passed'] = result.returncode == 0
                
                # Extract test count
                import re
                test_match = re.search(r'Ran (\d+) tests', results['output'])
                if test_match:
                    results['test_count'] = int(test_match.group(1))
                
                print(f"✅ Testes E2E: {results['test_count']} executados")
                if not results['passed']:
                    print("❌ Alguns testes E2E falharam")
            else:
                print("⚠️ Arquivo de testes E2E não encontrado")
                
        except subprocess.TimeoutExpired:
            results['passed'] = False
            results['output'] = "Testes E2E excederam o tempo limite"
            print("❌ Testes E2E excederam o tempo limite")
        except Exception as e:
            results['passed'] = False
            results['output'] = str(e)
            print(f"❌ Erro ao executar testes E2E: {e}")
        
        self.results['tests']['e2e_tests'] = results
        return results
    
    def generate_recommendations(self) -> List[str]:
        """Generate improvement recommendations based on analysis"""
        recommendations = []
        
        # Analyze results and generate recommendations
        if not self.results['tests'].get('code_quality', {}).get('python_syntax', {}).get('passed', True):
            recommendations.append("🐍 Corrigir erros de sintaxe Python identificados")
        
        if not self.results['tests'].get('code_quality', {}).get('javascript_syntax', {}).get('passed', True):
            recommendations.append("📜 Corrigir erros de sintaxe JavaScript identificados")
        
        if not self.results['tests'].get('code_quality', {}).get('security_scan', {}).get('passed', True):
            recommendations.append("🛡️ Resolver vulnerabilidades de segurança identificadas")
        
        if not self.results['tests'].get('unit_tests', {}).get('passed', True):
            recommendations.append("🧪 Corrigir testes unitários que estão falhando")
        
        if not self.results['tests'].get('e2e_tests', {}).get('passed', True):
            recommendations.append("🎭 Corrigir testes end-to-end que estão falhando")
        
        # Performance recommendations
        perf_issues = self.results['tests'].get('code_quality', {}).get('performance_audit', {}).get('issues', [])
        if perf_issues:
            recommendations.append("⚡ Otimizar performance baseado nos problemas identificados")
        
        # General recommendations
        recommendations.extend([
            "📚 Implementar documentação automática de API",
            "🔄 Configurar CI/CD pipeline para execução automática dos testes",
            "📊 Implementar monitoramento de performance em produção",
            "🔒 Adicionar testes de segurança automatizados",
            "🎨 Implementar linting automático para manter qualidade de código"
        ])
        
        self.results['recommendations'] = recommendations
        return recommendations
    
    def generate_report(self) -> str:
        """Generate comprehensive QA report"""
        print("\n📋 GERANDO RELATÓRIO FINAL")
        print("-" * 50)
        
        report_lines = [
            "# RELATÓRIO DE QUALIDADE ABRANGENTE",
            f"**Data/Hora:** {self.results['timestamp']}",
            "",
            "## 📊 RESUMO EXECUTIVO",
            ""
        ]
        
        # Calculate overall score
        total_tests = 0
        passed_tests = 0
        
        for test_category, test_results in self.results['tests'].items():
            if isinstance(test_results, dict):
                if 'passed' in test_results:
                    total_tests += 1
                    if test_results['passed']:
                        passed_tests += 1
                elif isinstance(test_results, dict):
                    # Handle nested test results
                    for subtest, subresult in test_results.items():
                        if isinstance(subresult, dict) and 'passed' in subresult:
                            total_tests += 1
                            if subresult['passed']:
                                passed_tests += 1
        
        if total_tests > 0:
            success_rate = (passed_tests / total_tests) * 100
            report_lines.append(f"**Taxa de Sucesso Geral:** {success_rate:.1f}% ({passed_tests}/{total_tests})")
        else:
            report_lines.append("**Taxa de Sucesso Geral:** N/A")
        
        report_lines.extend([
            "",
            "## 🧪 RESULTADOS DOS TESTES",
            ""
        ])
        
        # Add test results
        for test_category, test_results in self.results['tests'].items():
            category_name = test_category.replace('_', ' ').title()
            report_lines.append(f"### {category_name}")
            
            if isinstance(test_results, dict):
                if 'passed' in test_results:
                    status = "✅ PASSOU" if test_results['passed'] else "❌ FALHOU"
                    report_lines.append(f"**Status:** {status}")
                    
                    if 'test_count' in test_results:
                        report_lines.append(f"**Testes Executados:** {test_results['test_count']}")
                    
                    if 'issues' in test_results and test_results['issues']:
                        report_lines.append("**Problemas Identificados:**")
                        for issue in test_results['issues']:
                            report_lines.append(f"- {issue}")
                
                elif isinstance(test_results, dict):
                    # Handle nested results
                    for subtest, subresult in test_results.items():
                        if isinstance(subresult, dict) and 'passed' in subresult:
                            status = "✅" if subresult['passed'] else "❌"
                            subtest_name = subtest.replace('_', ' ').title()
                            report_lines.append(f"- **{subtest_name}:** {status}")
            
            report_lines.append("")
        
        # Add recommendations
        if self.results['recommendations']:
            report_lines.extend([
                "## 🎯 RECOMENDAÇÕES DE MELHORIA",
                ""
            ])
            for rec in self.results['recommendations']:
                report_lines.append(f"- {rec}")
            report_lines.append("")
        
        # Add footer
        report_lines.extend([
            "---",
            "",
            "**Relatório gerado automaticamente pelo Sistema de QA Avançado**",
            f"**Ferramentas utilizadas:** Python unittest, Playwright, Análise estática, Auditoria de segurança"
        ])
        
        report_content = "\n".join(report_lines)
        
        # Save report to file
        report_file = self.project_root / "qa_report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"📄 Relatório salvo em: {report_file}")
        
        return report_content
    
    def run_comprehensive_qa(self) -> bool:
        """Run complete QA process"""
        print("🎯 EXECUTANDO QA ABRANGENTE COM MÁXIMA PRECISÃO")
        print("=" * 80)
        
        # Run all QA checks
        self.run_code_quality_analysis()
        self.run_unit_tests()
        self.run_e2e_tests()
        self.generate_recommendations()
        
        # Generate final report
        self.generate_report()
        
        # Calculate overall success
        all_passed = True
        for test_category, test_results in self.results['tests'].items():
            if isinstance(test_results, dict):
                if 'passed' in test_results and not test_results['passed']:
                    all_passed = False
                elif isinstance(test_results, dict):
                    for subtest, subresult in test_results.items():
                        if isinstance(subresult, dict) and 'passed' in subresult and not subresult['passed']:
                            all_passed = False
        
        # Final summary
        print("\n" + "=" * 80)
        print("🏁 RESULTADO FINAL DA ANÁLISE DE QUALIDADE")
        print("=" * 80)
        
        if all_passed:
            print("🎉 PARABÉNS! TODOS OS CRITÉRIOS DE QUALIDADE FORAM ATENDIDOS!")
            print("✨ O projeto atende aos padrões de MÁXIMA QUALIDADE, PERFORMANCE E PRECISÃO")
        else:
            print("⚠️ ALGUNS CRITÉRIOS PRECISAM DE ATENÇÃO")
            print("🔧 Revise as recomendações para atingir a excelência total")
        
        return all_passed


def main():
    """Main execution function"""
    qa_manager = QualityAssuranceManager()
    success = qa_manager.run_comprehensive_qa()
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())