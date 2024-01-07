# vesselasid

vesselasid is a python client for the [Elektron ASID protocol](http://paulus.kapsi.fi/asid_protocol.txt), which allows programming SID registers remotely using MIDI Sysex (in an ASID receiver, such as a SidStation or [Vessel](https://github.com/anarkiwi/vessel) equipped C64 runing [VAP](https://github.com/anarkiwi/vap)).

It contains extensions that allow sending arbitrary data such as machine code over Sysex, and executing code remotely, and acknowledging commands with MIDI clock. Currently only VAP implements these extensions.

# programming registers

```
MIDI_DEV = "Scarlett 2i4 USB:Scarlett 2i4 USB MIDI 1 16:0"
port = mido.open_output(MIDI_DEV)
asid = Asid(port)
asid.start()
asid.sid.voice[1].set_state(freq=2048, s=15)
asid.sid.set_state(vol=15)
asid.update() # sends all pending changes
```

# sending and running machine code

```
MIDI_DEV = "Scarlett 2i4 USB:Scarlett 2i4 USB MIDI 1 16:0"
port = mido.open_output(MIDI_DEV)
in_port = mido.open_input(MIDI_DEV) # when in_port defined, receiver will acknowledge commands with MIDI clock.
asid = Asid(port, in_port=in_port)
asid.start()
code = xa(["lda #$0f", "sta $d418"]) # Asid adds rts automatically. Code origin currently fixed to $c000.
asid.load(code)
asid.run() # does jsr $c000 remotely, sends clock when done.
```
