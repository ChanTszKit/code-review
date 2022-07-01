#### Necessary packages


```python
import miditoolkit
import utils
```

#### Read midi


```python
file_name = "196.mid"
midi_obj = miditoolkit.midi.parser.MidiFile(file_name)
```

#### Read raw token


```python
note_raw, tempo_raw = utils.read_items(file_name)

# Peek the first 3 raw tokens
note_raw[0:3]
```




    [Item(name=Note, start=0, end=1680, velocity=56, pitch=51, Type=2, Program=-1, Time Signature=00),
     Item(name=Note, start=0, end=2040, velocity=62, pitch=58, Type=2, Program=-1, Time Signature=00),
     Item(name=Note, start=0, end=600, velocity=56, pitch=63, Type=2, Program=-1, Time Signature=00)]



#### Read 'Program' to the raw token
Observation:
- *Type=2* indicates it belongs to the thrid channel.

P.S. 'Program' is appended into each note.


```python
def Type2Program(midi_obj, channel):
    '''Get Program Change Number from the instrument name at a specified channel
    
    Parameters:
        midi_obj (MidiFile): from miditoolkit.midi.parser.MidiFile
        channel (int): the index of the channel, 0-based
        
    Returns:
        int: Program Change Number, 0-based
    
    '''
    instrument = midi_obj.instruments[channel]
    
    # Assume Acoustic Grand Piano only
    return 0
    
    if instrument.name == "piano": # Acoustic Grand Piano
        return 0
    
    # TODO: support other program change number
    return -1
```


```python
# Add 'Program' to each raw token
for i in note_raw:
    i.Program = Type2Program(midi_obj, i.Type)

# Peek the first 3 modified raw tokens
note_raw[0:3]
```




    [Item(name=Note, start=0, end=1680, velocity=56, pitch=51, Type=2, Program=0, Time Signature=00),
     Item(name=Note, start=0, end=2040, velocity=62, pitch=58, Type=2, Program=0, Time Signature=00),
     Item(name=Note, start=0, end=600, velocity=56, pitch=63, Type=2, Program=0, Time Signature=00)]



#### Read 'Time Signature' to the raw token
P.S. 'Time Signature' is appended into each note.


```python
def raw_time_signature(midi_obj, time):
    '''Get Time Signature at a specified time

    Parameters:
        midi_obj (MidiFile): from miditoolkit.midi.parser.MidiFile
        time (int): the acquired time
        
    Returns:
        str: the Time Signature at that time
    
    '''
    ts_list = [i.time for i in midi_obj.time_signature_changes]
    
    idx = -1
    if time >= ts_list[-1]:
    # It belongs to the last time signature
        idx = len(ts_list)-1
    else: 
    # It belongs to a specific interval
        for i in range(len(ts_list)):    
            if time >= ts_list[i] and time < ts_list[i+1]:
                idx = i
                break
            
    numerator = midi_obj.time_signature_changes[idx].numerator
    denominator = midi_obj.time_signature_changes[idx].denominator
    return f"{numerator}{denominator}"
```


```python
# Add 'TimeSignature' to each raw token
for i in note_raw:
    i.TimeSignature = raw_time_signature(midi_obj, i.start)

# Peek the first 3 modified raw tokens
note_raw[0:3]
```




    [Item(name=Note, start=0, end=1680, velocity=56, pitch=51, Type=2, Program=0, Time Signature=44),
     Item(name=Note, start=0, end=2040, velocity=62, pitch=58, Type=2, Program=0, Time Signature=44),
     Item(name=Note, start=0, end=600, velocity=56, pitch=63, Type=2, Program=0, Time Signature=44)]



#### Next step: Generate sequence
i.e. utils.py -> def item2event


```python
# Slice notes into groups
note_groups = utils.group_items(items=note_raw, max_time=note_raw[-1].end)
# Generate sequence
sequence = utils.item2event(groups=note_groups, task='custom')

# Peek the first 3 sequence
sequence[0:3]
```




    [[Event(name=Bar, time=None, value=New, text=1, Type=-1),
      Event(name=Position, time=0, value=1/24, text=0, Type=-1),
      Event(name=Pitch, time=0, value=51, text=51, Type=-1),
      Event(name=Duration, time=0, value=27, text=1680/1680, Type=-1),
      Event(name=Program, time=0, value=0, text=0, Type=-1),
      Event(name=Time Signature, time=0, value=44, text=44, Type=-1)],
     [Event(name=Bar, time=None, value=Continue, text=1, Type=-1),
      Event(name=Position, time=0, value=1/24, text=0, Type=-1),
      Event(name=Pitch, time=0, value=58, text=58, Type=-1),
      Event(name=Duration, time=0, value=33, text=2040/2040, Type=-1),
      Event(name=Program, time=0, value=0, text=0, Type=-1),
      Event(name=Time Signature, time=0, value=44, text=44, Type=-1)],
     [Event(name=Bar, time=None, value=Continue, text=1, Type=-1),
      Event(name=Position, time=0, value=1/24, text=0, Type=-1),
      Event(name=Pitch, time=0, value=63, text=63, Type=-1),
      Event(name=Duration, time=0, value=9, text=600/600, Type=-1),
      Event(name=Program, time=0, value=0, text=0, Type=-1),
      Event(name=Time Signature, time=0, value=44, text=44, Type=-1)]]


