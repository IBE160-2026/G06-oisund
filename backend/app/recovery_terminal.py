"""Linux controlling-terminal delivery; TTY presence cannot detect recording."""
import os
import signal
import termios
import time
from datetime import timezone
from uuid import uuid4

from . import password_recovery as recovery

DIALOGUE_SECONDS = 300


class Terminal:
    def __enter__(self):
        self.alternate = False
        if not all(os.isatty(fd) for fd in (0, 1, 2)):
            raise recovery.RecoveryError('Krever interaktiv terminal uten omdirigering.')
        self.fd = os.open('/dev/tty', os.O_RDWR | os.O_NOCTTY)
        try:
            # /dev/tty is an alias device, so its st_rdev differs from /dev/pts/N.
            if (len({os.ttyname(fd) for fd in (0, 1, 2)}) != 1
                    or any(os.tcgetpgrp(fd) != os.getpgrp() for fd in (0, 1, 2, self.fd))):
                raise recovery.RecoveryError('Alle strømmer må bruke styrende terminal.')
            self.settings = termios.tcgetattr(self.fd)
            hidden = termios.tcgetattr(self.fd)
            hidden[3] &= ~termios.ECHO
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, hidden)
        except BaseException:
            os.close(self.fd)
            raise
        return self

    def write(self, text):
        data = text.encode('utf-8')
        while data:
            sent = os.write(self.fd, data)
            if not sent:
                raise OSError('Terminal unavailable')
            data = data[sent:]

    def read(self, prompt):
        self.write(prompt)
        result = bytearray()
        while len(result) <= 400:
            char = os.read(self.fd, 1)
            if char in (b'', b'\x04'):
                raise recovery.RecoveryError('Avbrutt.')
            if char == b'\n':
                self.write('\n')
                return result.decode('utf-8')
            result.extend(char)
        raise recovery.RecoveryError('Avbrutt.')

    def clear(self):
        if self.alternate:
            self.write('\x1b[2J\x1b[H\x1b[?1049l')
            self.alternate = False

    def begin_secret(self):
        self.alternate = True  # Also attempt restoration after a partial write.
        self.write('\x1b[?1049h\x1b[2J\x1b[H')

    def __exit__(self, *args):
        try:
            self.clear()
        finally:
            try:
                termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.settings)
            finally:
                os.close(self.fd)


def run(action, username):
    target = None
    attempted = False
    revoke_attempted = False
    proof_id = None
    def interrupted(*_):
        signal.setitimer(signal.ITIMER_REAL, 0)
        raise KeyboardInterrupt()
    def timeout(*_):
        raise recovery.RecoveryError('Tidsfristen er utløpt. Start på nytt og bekreft kontoen igjen.')
    previous = {sig: signal.signal(sig, interrupted) for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGTSTP)}
    previous[signal.SIGALRM] = signal.signal(signal.SIGALRM, timeout)
    deadline = time.monotonic() + DIALOGUE_SECONDS
    signal.setitimer(signal.ITIMER_REAL, DIALOGUE_SECONDS)
    try:
        with Terminal() as terminal:
            target = recovery.resolve(username)
            terminal.write(f"Konto: {target['username']}\nUUID: {target['id']}\nVertskontekst: {recovery.host_actor()} (ikke bekreftet SSH-person)\n")
            if terminal.read('Skriv hele brukernavnet for å bekrefte (tomt avbryter): ') != target['username']:
                raise recovery.RecoveryError('Bekreftelsen stemmer ikke. Avbrutt.')
            if action == 'recovery-revoke':
                revoke_attempted = True
                recovery.revoke(target)
                terminal.write('Alle utestående koder er tilbakekalt. Passord og økter er uendret.\n')
                return
            if terminal.read('Bekreft identitet, trygg direkte overlevering og INGEN opptak/transkripsjon/delt skjerm/CI/utklippstavlehistorikk. TTY beviser ikke dette. Skriv TRYGT: ') != 'TRYGT':
                raise recovery.RecoveryError('Forhåndskontroll ikke bekreftet. Avbrutt.')
            proof_id = uuid4()  # Known even if commit acknowledgement is lost.
            attempted = True
            try:
                code, proof = recovery.issue(target, proof_id)
            except recovery.RecoveryError:
                attempted = False  # Known rejection; prior valid proof stays unchanged.
                raise
            proof_id = proof['id']
            checked_at = time.monotonic()
            remaining = recovery.delivery(target, proof_id)
            display_budget = min(deadline, checked_at + remaining) - time.monotonic()
            if display_budget <= 0:
                timeout()
            signal.setitimer(signal.ITIMER_REAL, display_budget)
            terminal.begin_secret()
            terminal.write(f"Engangskode: {code}\nUtløper: {proof['expires_at'].astimezone(timezone.utc).isoformat()} (UTC)\n")
            code = None
            if terminal.read('Skriv MOTTATT etter trygg overlevering for å tømme skjermen: ') != 'MOTTATT':
                raise recovery.RecoveryError('Overlevering ikke bekreftet.')
            terminal.clear()
            recovery.delivery(target, proof_id, acknowledge=True)
            terminal.write('Overlevering bekreftet; kodevisningen er tømt. Passord og økter er uendret.\n')
        attempted = False  # Includes successful terminal clear/restore/close.
    except BaseException as exc:
        signal.setitimer(signal.ITIMER_REAL, 0)
        if revoke_attempted:
            message = 'USIKKER tilbakekalling. Kjør recovery-revoke for nøyaktig konto på nytt; ikke anta at koden er tilbakekalt.'
        elif attempted and target:
            try:
                recovery.revoke(target, proof_id, 'delivery', 'failed')
                message = 'Utstedelse/overlevering avbrutt eller kode ikke lenger gyldig; denne utstedelsen er tilbakekalt. Bekreft kontoen og utsted ny kode ved behov.'
            except BaseException:
                message = 'USIKKER utstedelse. Kjør recovery-revoke for nøyaktig konto før nytt forsøk; kode utløper senest etter 30 minutter.'
        else:
            message = str(exc) if isinstance(exc, recovery.RecoveryError) else 'Avbrutt. Ingen kode vist.'
        raise SystemExit(message) from None
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        for sig, handler in previous.items():
            signal.signal(sig, handler)
