import MIDI
import settings
#from Logging import log

import Control

class GlobalControl(Control):
	__module__ = __name__
	__doc__ = "Global parameters of SelectedTrackControl"

	def __init__(self, c_instance, selected_track_controller):
		super(c_instance, selected_track_controller)
		
		# each callback is (key, callback)
		# key is a key in settings.midi_mapping
		self.midi_callbacks = (
			("overdub", self.toggle_overdub),
			("disable_overdub", self.disable_overdub),
			("record", self.toggle_record),
			
			("punch_in", self.toggle_punchin),
			("punch_out", self.toggle_punchout),
			
			("metronome", self.toggle_metronome),
			("loop", self.toggle_loop),
			
			
			("loop_move", self.move_loop_by),
			("loop_lb_move", self.move_loop_left_bracket_by),
			("loop_rb_move", self.move_loop_right_bracket_by),
			("tempo", self.set_tempo)
		)
		
		# steps, when ABSOLUTE mode for tempo CC is used
		self.tempo_step = (settings.tempo_max - settings.tempo_min)/127
		
		# register midi_callbacks via parent
		self.register_midi_callbacks()
	
	
	
	
	
	
	def toggle_overdub(self, value, mode):
		self.song.overdub = not self.song.overdub
	
	def disable_overdub(self, value, mode):
		self.song.overdub = 0
	
	
	def toggle_record(self, value, mode):
		self.song.record_mode = not self.song.record_mode
	def toggle_punchin(self, value, mode):
		self.song.punch_in = not self.song.punch_in
	def toggle_punchout(self, value, mode):
		self.song.punch_out = not self.song.punch_out
		
	def toggle_metronome(self, value, mode):
		self.song.metronome = not self.song.metronome
	
	def toggle_loop(self, value, mode):
		self.song.loop = not self.song.loop
		
	def move_loop_by(self, value, mode):
		self.song.loop_start = self.song.loop_start + MIDI.relative_to_signed_int[mode](value)
		
	def move_loop_left_bracket_by(self, value, mode):
		d_value = MIDI.relative_to_signed_int[mode](value)
		self.move_loop_by(d_value)
		self.move_loop_right_bracket_by(-d_value)
	
	def move_loop_right_bracket_by(self, value, mode):
		self.song.loop_length = self.song.loop_length + MIDI.relative_to_signed_int[mode](value)
	
	def set_tempo(self, value, mode):
		if mode == MIDI.ABSOLUTE:
			self.song.tempo = settings.tempo_min + value*self.tempo_step
		else:
			self.song.tempo = self.song.tempo + MIDI.relative_to_signed_int[mode](value)
	