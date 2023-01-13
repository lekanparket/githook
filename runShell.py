#!/Users/akindele214/Desktop/Dev/gitsecure/env/bin/python3
import re

import re
import os, subprocess
from subprocess import Popen, PIPE

secret_key_regex = "(?:[0–9a-z\-_\t .]{0,20})(?:[\s|']|[\s|\"]){0,3}(?:=|>|:=|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9_-]{32})(?:['|\"|\n|\r|\s|\x60]|$)"

secret_key_dict = {
    "Cloudinary"  : "cloudinary://.*",
	"Firebase URL": ".*firebaseio\.com",
	"Slack Token": "(xox[p|b|o|a]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32})",
	"RSA private key": "-----BEGIN RSA PRIVATE KEY-----",
	"SSH (DSA) private key": "-----BEGIN DSA PRIVATE KEY-----",
	"SSH (EC) private key": "-----BEGIN EC PRIVATE KEY-----",
	"PGP private key block": "-----BEGIN PGP PRIVATE KEY BLOCK-----",
	"Amazon AWS Access Key ID": "AKIA[0-9A-Z]{16}",
	"Amazon MWS Auth Token": "amzn\\.mws\\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
	"AWS API Key": "AKIA[0-9A-Z]{16}",
	"Facebook Access Token": "EAACEdEose0cBA[0-9A-Za-z]+",
	"Facebook OAuth": "[f|F][a|A][c|C][e|E][b|B][o|O][o|O][k|K].*['|\"][0-9a-f]{32}['|\"]",
	"GitHub": "[g|G][i|I][t|T][h|H][u|U][b|B].*['|\"][0-9a-zA-Z]{35,40}['|\"]",
	"Generic API Key": "[a|A][p|P][i|I][_]?[k|K][e|E][y|Y].*['|\"][0-9a-zA-Z]{32,45}['|\"]",
	"Generic Secret": "[s|S][e|E][c|C][r|R][e|E][t|T].*['|\"][0-9a-zA-Z]{32,45}['|\"]",
	"Google API Key": "AIza[0-9A-Za-z\\-_]{35}",
	"Google Cloud Platform API Key": "AIza[0-9A-Za-z\\-_]{35}",
	"Google Cloud Platform OAuth": "[0-9]+-[0-9A-Za-z_]{32}\\.apps\\.googleusercontent\\.com",
	"Google Drive API Key": "AIza[0-9A-Za-z\\-_]{35}",
	"Google Drive OAuth": "[0-9]+-[0-9A-Za-z_]{32}\\.apps\\.googleusercontent\\.com",
	"Google (GCP) Service-account": "\"type\": \"service_account\"",
	"Google Gmail API Key": "AIza[0-9A-Za-z\\-_]{35}",
	"Google Gmail OAuth": "[0-9]+-[0-9A-Za-z_]{32}\\.apps\\.googleusercontent\\.com",
	"Google OAuth Access Token": "ya29\\.[0-9A-Za-z\\-_]+",
	"Google YouTube API Key": "AIza[0-9A-Za-z\\-_]{35}",
	"Google YouTube OAuth": "[0-9]+-[0-9A-Za-z_]{32}\\.apps\\.googleusercontent\\.com",
	"Heroku API Key": "[h|H][e|E][r|R][o|O][k|K][u|U].*[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}",
	"MailChimp API Key": "[0-9a-f]{32}-us[0-9]{1,2}",
	"Mailgun API Key": "key-[0-9a-zA-Z]{32}",
	"Password in URL": "[a-zA-Z]{3,10}://[^/\\s:@]{3,20}:[^/\\s:@]{3,20}@.{1,100}[\"'\\s]",
	"PayPal Braintree Access Token": "access_token\\$production\\$[0-9a-z]{16}\\$[0-9a-f]{32}",
	"Picatic API Key": "sk_live_[0-9a-z]{32}",
	"Slack Webhook": "https://hooks.slack.com/services/T[a-zA-Z0-9_]{8}/B[a-zA-Z0-9_]{8}/[a-zA-Z0-9_]{24}",
	"Stripe API Key": "sk_live_[0-9a-zA-Z]{24}",
	"Stripe Restricted API Key": "rk_live_[0-9a-zA-Z]{24}",
	"Square Access Token": "sq0atp-[0-9A-Za-z\\-_]{22}",
	"Square OAuth Secret": "sq0csp-[0-9A-Za-z\\-_]{43}",
	"Twilio API Key": "SK[0-9a-fA-F]{32}",
	"Twitter Access Token": "[t|T][w|W][i|I][t|T][t|T][e|E][r|R].*[1-9][0-9]+-[0-9a-zA-Z]{40}",
	"Twitter OAuth": "[t|T][w|W][i|I][t|T][t|T][e|E][r|R].*['|\"][0-9a-zA-Z]{35,44}['|\"]"
}

secret_key_keys = list(secret_key_dict.keys())
secret_key_vals = secret_key_dict.values()

extension_list =  ['.abap', '.asc', '.ash', '.ampl', '.mod', '.g4', '.apib', '.apl', '.dyalog', '.asp', '.asax', '.ascx', '.ashx', '.asmx', '.aspx', '.axd', '.dats', '.hats', '.sats', '.as', '.adb', '.ada', '.ads', '.agda', '.als', '.apacheconf', '.vhost', '.cls', '.applescript', '.scpt', '.arc', '.ino', '.asciidoc', '.adoc', '.asc', '.aj', '.asm', '.a51', '.inc', '.nasm', '.aug', '.ahk', '.ahkl', '.au3', '.awk', '.auk', '.gawk', '.mawk', '.nawk', '.bat', '.cmd', '.befunge', '.bison', '.bb', '.bb', '.decls', '.bmx', '.bsv', '.boo', '.b', '.bf', '.brs', '.bro', '.c', '.cats', '.h', '.idc', '.w', '.cs', '.cake', '.cshtml', '.csx', '.cpp', '.c++', '.cc', '.cp', '.cxx', '.h', '.h++', '.hh', '.hpp', '.hxx', '.inc', '.inl', '.ipp', '.tcc', '.tpp', '.c-objdump', '.chs', '.clp', '.cmake', '.cmake.in', '.cob', '.cbl', '.ccp', '.cobol', '.cpy', '.css', '.csv', '.capnp', '.mss', '.ceylon', '.chpl', '.ch', '.ck', '.cirru', '.clw', '.icl', '.dcl', '.click', '.clj', '.boot', '.cl2', '.cljc', '.cljs', '.cljs.hl', '.cljscm', '.cljx', '.hic', '.coffee', '._coffee', '.cake', '.cjsx', '.cson', '.iced', '.cfm', '.cfml', '.cfc', '.lisp', '.asd', '.cl', '.l', '.lsp', '.ny', '.podsl', '.sexp', '.cp', '.cps', '.cl', '.coq', '.v', '.cppobjdump', '.c++-objdump', '.c++objdump', '.cpp-objdump', '.cxx-objdump', '.creole', '.cr', '.feature', '.cu', '.cuh', '.cy', '.pyx', '.pxd', '.pxi', '.d', '.di', '.d-objdump', '.com', '.dm', '.zone', '.arpa', '.d', '.darcspatch', '.dpatch', '.dart', '.diff', '.patch', '.dockerfile', '.djs', '.dylan', '.dyl', '.intr', '.lid', '.E', '.ecl', '.eclxml', '.ecl', '.sch', '.brd', '.epj', '.e', '.ex', '.exs', '.elm', '.el', '.emacs', '.emacs.desktop', '.em', '.emberscript', '.erl', '.es', '.escript', '.hrl', '.xrl', '.yrl', '.fs', '.fsi', '.fsx', '.fx', '.flux', '.f90', '.f', '.f03', '.f08', '.f77', '.f95', '.for', '.fpp', '.factor', '.fy', '.fancypack', '.fan', '.fs', '.for', '.eam.fs', '.fth', '.4th', '.f', '.for', '.forth', '.fr', '.frt', '.fs', '.ftl', '.fr', '.g', '.gco', '.gcode', '.gms', '.g', '.gap', '.gd', '.gi', '.tst', '.s', '.ms', '.gd', '.glsl', '.fp', '.frag', '.frg', '.fs', '.fsh', '.fshader', '.geo', '.geom', '.glslv', '.gshader', '.shader', '.vert', '.vrx', '.vsh', '.vshader', '.gml', '.kid', '.ebuild', '.eclass', '.po', '.pot', '.glf', '.gp', '.gnu', '.gnuplot', '.plot', '.plt', '.go', '.golo', '.gs', '.gst', '.gsx', '.vark', '.grace', '.gradle', '.gf', '.gml', '.graphql', '.dot', '.gv', '.man', '.1', '.1in', '.1m', '.1x', '.2', '.3', '.3in', '.3m', '.3qt', '.3x', '.4', '.5', '.6', '.7', '.8', '.9', '.l', '.me', '.ms', '.n', '.rno', '.roff', '.groovy', '.grt', '.gtpl', '.gvy', '.gsp', '.hcl', '.tf', '.hlsl', '.fx', '.fxh', '.hlsli', '.html', '.htm', '.html.hl', '.inc', '.st', '.xht', '.xhtml', '.mustache', '.jinja', '.eex', '.erb', '.erb.deface', '.phtml', '.http', '.hh', '.php', '.haml', '.haml.deface', '.handlebars', '.hbs', '.hb', '.hs', '.hsc', '.hx', '.hxsl', '.hy', '.bf', '.pro', '.dlm', '.ipf', '.ini', '.cfg', '.prefs', '.pro', '.properties', '.irclog', '.weechatlog', '.idr', '.lidr', '.ni', '.i7x', '.iss', '.io', '.ik', '.thy', '.ijs', '.flex', '.jflex', '.json', '.geojson', '.lock', '.topojson', '.json5', '.jsonld', '.jq', '.jsx', '.jade', '.j', '.java', '.jsp', '.js', '._js', '.bones', '.es', '.es6', '.frag', '.gs', '.jake', '.jsb', '.jscad', '.jsfl', '.jsm', '.jss', '.njs', '.pac', '.sjs', '.ssjs', '.sublime-build', '.sublime-commands', '.sublime-completions', '.sublime-keymap', '.sublime-macro', '.sublime-menu', '.sublime-mousemap', '.sublime-project', '.sublime-settings', '.sublime-theme', '.sublime-workspace', '.sublime_metrics', '.sublime_session', '.xsjs', '.xsjslib', '.jl', '.ipynb', '.krl', '.sch', '.brd', '.kicad_pcb', '.kit', '.kt', '.ktm', '.kts', '.lfe', '.ll', '.lol', '.lsl', '.lslp', '.lvproj', '.lasso', '.las', '.lasso8', '.lasso9', '.ldml', '.latte', '.lean', '.hlean', '.less', '.l', '.lex', '.ly', '.ily', '.b', '.m', '.ld', '.lds', '.mod', '.liquid', '.lagda', '.litcoffee', '.lhs', '.ls', '._ls', '.xm', '.x', '.xi', '.lgt', '.logtalk', '.lookml', '.ls', '.lua', '.fcgi', '.nse', '.pd_lua', '.rbxs', '.wlua', '.mumps', '.m', '.m4', '.m4', '.ms', '.mcr', '.mtml', '.muf', '.m', '.mak', '.d', '.mk', '.mkfile', '.mako', '.mao', '.md', '.markdown', '.mkd', '.mkdn', '.mkdown', '.ron', '.mask', '.mathematica', '.cdf', '.m', '.ma', '.mt', '.nb', '.nbp', '.wl', '.wlt', '.matlab', '.m', '.maxpat', '.maxhelp', '.maxproj', '.mxt', '.pat', '.mediawiki', '.wiki', '.m', '.moo', '.metal', '.minid', '.druby', '.duby', '.mir', '.mirah', '.mo', '.mod', '.mms', '.mmk', '.monkey', '.moo', '.moon', '.myt', '.ncl', '.nl', '.nsi', '.nsh', '.n', '.axs', '.axi', '.axs.erb', '.axi.erb', '.nlogo', '.nl', '.lisp', '.lsp', '.nginxconf', '.vhost', '.nim', '.nimrod', '.ninja', '.nit', '.nix', '.nu', '.numpy', '.numpyw', '.numsc', '.ml', '.eliom', '.eliomi', '.ml4', '.mli', '.mll', '.mly', '.objdump', '.m', '.h', '.mm', '.j', '.sj', '.omgrofl', '.opa', '.opal', '.cl', '.opencl', '.p', '.cls', '.scad', '.org', '.ox', '.oxh', '.oxo', '.oxygene', '.oz', '.pwn', '.inc', '.php', '.aw', '.ctp', '.fcgi', '.inc', '.php3', '.php4', '.php5', '.phps', '.phpt', '.pls', '.pck', '.pkb', '.pks', '.plb', '.plsql', '.sql', '.sql', '.pov', '.inc', '.pan', '.psc', '.parrot', '.pasm', '.pir', '.pas', '.dfm', '.dpr', '.inc', '.lpr', '.pp', '.pl', '.al', '.cgi', '.fcgi', '.perl', '.ph', '.plx', '.pm', '.pod', '.psgi', '.t', '.6pl', '.6pm', '.nqp', '.p6', '.p6l', '.p6m', '.pl', '.pl6', '.pm', '.pm6', '.t', '.pkl', '.l', '.pig', '.pike', '.pmod', '.pod', '.pogo', '.pony', '.ps', '.eps', '.ps1', '.psd1', '.psm1', '.pde', '.pl', '.pro', '.prolog', '.yap', '.spin', '.proto', '.asc', '.pub', '.pp', '.pd', '.pb', '.pbi', '.purs', '.py', '.bzl', '.cgi', '.fcgi', '.gyp', '.lmi', '.pyde', '.pyp', '.pyt', '.pyw', '.rpy', '.tac', '.wsgi', '.xpy', '.pytb', '.qml', '.qbs', '.pro', '.pri', '.r', '.rd', '.rsx', '.raml', '.rdoc', '.rbbas', '.rbfrm', '.rbmnu', '.rbres', '.rbtbar', '.rbuistate', '.rhtml', '.rmd', '.rkt', '.rktd', '.rktl', '.scrbl', '.rl', '.raw', '.reb', '.r', '.r2', '.r3', '.rebol', '.red', '.reds', '.cw', '.rpy', '.rs', '.rsh', '.robot', '.rg', '.rb', '.builder', '.fcgi', '.gemspec', '.god', '.irbrc', '.jbuilder', '.mspec', '.pluginspec', '.podspec', '.rabl', '.rake', '.rbuild', '.rbw', '.rbx', '.ru', '.ruby', '.thor', '.watchr', '.rs', '.rs.in', '.sas', '.scss', '.smt2', '.smt', '.sparql', '.rq', '.sqf', '.hqf', '.sql', '.cql', '.ddl', '.inc', '.prc', '.tab', '.udf', '.viw', '.sql', '.db2', '.ston', '.svg', '.sage', '.sagews', '.sls', '.sass', '.scala', '.sbt', '.sc', '.scaml', '.scm', '.sld', '.sls', '.sps', '.ss', '.sci', '.sce', '.tst', '.self', '.sh', '.bash', '.bats', '.cgi', '.command', '.fcgi', '.ksh', '.sh.in', '.tmux', '.tool', '.zsh', '.sh-session', '.shen', '.sl', '.slim', '.smali', '.st', '.cs', '.tpl', '.sp', '.inc', '.sma', '.nut', '.stan', '.ML', '.fun', '.sig', '.sml', '.do', '.ado', '.doh', '.ihlp', '.mata', '.matah', '.sthlp', '.styl', '.sc', '.scd', '.swift', '.sv', '.svh', '.vh', '.toml', '.txl', '.tcl', '.adp', '.tm', '.tcsh', '.csh', '.tex', '.aux', '.bbx', '.bib', '.cbx', '.cls', '.dtx', '.ins', '.lbx', '.ltx', '.mkii', '.mkiv', '.mkvi', '.sty', '.toc', '.tea', '.t', '.txt', '.fr', '.nb', '.ncl', '.no', '.textile', '.thrift', '.t', '.tu', '.ttl', '.twig', '.ts', '.tsx', '.upc', '.anim', '.asset', '.mat', '.meta', '.prefab', '.unity', '.uno', '.uc', '.ur', '.urs', '.vcl', '.vhdl', '.vhd', '.vhf', '.vhi', '.vho', '.vhs', '.vht', '.vhw', '.vala', '.vapi', '.v', '.veo', '.vim', '.vb', '.bas', '.cls', '.frm', '.frx', '.vba', '.vbhtml', '.vbs', '.volt', '.vue', '.owl', '.webidl', '.x10', '.xc', '.xml', '.ant', '.axml', '.ccxml', '.clixml', '.cproject', '.csl', '.csproj', '.ct', '.dita', '.ditamap', '.ditaval', '.dll.config', '.dotsettings', '.filters', '.fsproj', '.fxml', '.glade', '.gml', '.grxml', '.iml', '.ivy', '.jelly', '.jsproj', '.kml', '.launch', '.mdpolicy', '.mm', '.mod', '.mxml', '.nproj', '.nuspec', '.odd', '.osm', '.plist', '.pluginspec', '.props', '.ps1xml', '.psc1', '.pt', '.rdf', '.rss', '.scxml', '.srdf', '.storyboard', '.stTheme', '.sublime-snippet', '.targets', '.tmCommand', '.tml', '.tmLanguage', '.tmPreferences', '.tmSnippet', '.tmTheme', '.ts', '.tsx', '.ui', '.urdf', '.ux', '.vbproj', '.vcxproj', '.vssettings', '.vxml', '.wsdl', '.wsf', '.wxi', '.wxl', '.wxs', '.x3d', '.xacro', '.xaml', '.xib', '.xlf', '.xliff', '.xmi', '.xml.dist', '.xproj', '.xsd', '.xul', '.zcml', '.xsp-config', '.xsp.metadata', '.xpl', '.xproc', '.xquery', '.xq', '.xql', '.xqm', '.xqy', '.xs', '.xslt', '.xsl', '.xojo_code', '.xojo_menu', '.xojo_report', '.xojo_script', '.xojo_toolbar', '.xojo_window', '.xtend', '.yml', '.reek', '.rviz', '.sublime-syntax', '.syntax', '.yaml', '.yaml-tmlanguage', '.yang', '.y', '.yacc', '.yy', '.zep', '.zimpl', '.zmpl', '.zpl', '.desktop', '.desktop.in', '.ec', '.eh', '.edn', '.fish', '.mu', '.nc', '.ooc', '.rst', '.rest', '.rest.txt', '.rst.txt', '.wisp', '.prg', '.ch', '.prw']

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class GitSecureFileReader:
    def __init__(self, file_dir):
        self.dir = file_dir
    
    def file_opener(self):
        try:
            file1 = open(self.dir, 'r')
            return file1
        except Exception as e:
            print(f"Error opening file {e}")
            return None

    def file_reader(self):
        return self.file_opener().readlines()

    def detect_secret_keys(self):
        lines = self.file_reader()
        count = 0
        has_key = False

        for line in lines:
            count += 1
            z = re.match(secret_key_regex, line)

            for i, values in enumerate(secret_key_vals):
                vv = re.match(values, line)
                if vv:
                    has_key = True
                    print(bcolors.WARNING +"Warning: File directory "+ f"{self.dir}" +bcolors.ENDC)
                    print(bcolors.WARNING  + f"Warning: Line {count} has a {secret_key_keys[i]} " + bcolors.BOLD + 
                        bcolors.FAIL + f'{z.groups()[0]}', bcolors.ENDC + bcolors.WARNING +
                        "please have a look." + bcolors.ENDC)
                    break
            # if z:
            #     has_key = True
            #     print(bcolors.WARNING +"Warning: File directory "+ f"{self.dir}" +bcolors.ENDC)
            #     print(bcolors.WARNING  + f"Warning: Line {count} has a secret key " + bcolors.BOLD + 
            #             bcolors.FAIL + f'{z.groups()[0]}', bcolors.ENDC + bcolors.WARNING +
            #             "please have a look." + bcolors.ENDC)
        
        if has_key is False:
            print(bcolors.OKGREEN+f"YAY!!!!!! No secret key found in {self.dir.split('/')[-1]}"+bcolors.ENDC)



session = subprocess.Popen(['sh', './gitSearch.sh'], stdout=PIPE, stderr=PIPE)
stdout, stderr = session.communicate()

if stderr:
    raise Exception("Error "+str(stderr))
else:
    print(3333)
    output = stdout.decode().split('\n')
    if len(output) > 3:
        last_outputs = output[:-2]
        files_changes = []
        current_dir = os.getcwd()
        for last_output in last_outputs:
            last_output = last_output.split('|')[0].replace(' ', '')
            file_extension = last_output.split('.')[-1:]

            if file_extension in extension_list:
                gcfr = GitSecureFileReader(f'{current_dir}/{last_output}')
                gcfr.detect_secret_keys()
