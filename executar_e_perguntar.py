import sys
import subprocess

proc = subprocess.Popen(sys.argv[1])
proc.communicate()

print("\n==========================================\nAperte enter para continuar...")
sys.stdin.readline()
