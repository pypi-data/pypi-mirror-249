from typing import Optional

from vispunk_motion.custom_nodes.ComfyUI_Advanced_ControlNet.control.nodes import (
    TimestepKeyframeNode,
    LatentKeyframeNode,
)
from vispunk_motion.custom_nodes.ComfyUI_FizzNodes.ScheduledNodes import BatchPromptSchedule
from vispunk_motion.custom_nodes.custom.nodes import (
    ControlNetLoaderAdvanced,
    LoadPILImage,
)
from vispunk_motion.nodes import (
    ConditioningZeroOut,
    ControlNetApplyAdvanced,
    CLIPTextEncode,
    LoadImage,
)


class Prompt:
    def __init__(self, prompt: str = "", negative_prompt: str = "", CLIP = None):
        self.prompt = prompt
        self.negative_prompt = negative_prompt
        self.CLIP = CLIP

    def encode(self, animator):
        (positive,) = CLIPTextEncode().encode(self.CLIP or animator.clip, self.prompt)
        (negative,) = CLIPTextEncode().encode(self.CLIP or animator.clip, self.negative_prompt)
        return positive, negative


class PromptTravel(Prompt):
    def __init__(self, prompt_schedule: str = "", pre_text: str = "", app_text: str = "", negative_prompt: str = "", max_frames: int = 100, CLIP = None):
        self.prompt_schedule = prompt_schedule
        self.pre_text = pre_text
        self.app_text = app_text
        self.negative_prompt = negative_prompt
        self.max_frames = max_frames
        self.CLIP = CLIP

    def encode(self, animator):
        (positive,) = BatchPromptSchedule().animate(
            self.prompt_schedule,
            self.max_frames,
            self.CLIP or animator.clip,
            pw_a=0,
            pw_b=0,
            pw_c=0,
            pw_d=0,
            pre_text=self.pre_text,
            app_text=self.app_text,
        )
        (negative,) = CLIPTextEncode().encode(self.CLIP or animator.clip, self.negative_prompt)
        return positive, negative


class ConditioningStack:
    def __init__(self, conditions = []):
        self.conditions = conditions
    
    def add(self, condition):
        self.conditions.append(condition)

    def encode(self, animator):
        # Initialize encodings to zero
        if not len(self.conditions):
            (cond,) = CLIPTextEncode().encode(animator.clip, "")
            (zero_cond,) = ConditioningZeroOut().zero_out(cond)
            positive = negative = zero_cond
        prompt_conditions = [condition for condition in self.conditions if isinstance(condition, Prompt)]
        if len(prompt_conditions) > 1:
            raise ValueError("More than one Prompt found")
        other_conditions = [condition for condition in self.conditions if not isinstance(condition, Prompt)]
        # Start with prompt encoding if available
        if len(prompt_conditions) == 1:
            positive, negative = prompt_conditions[0].encode(animator)
        for condition in other_conditions:
            positive, negative = condition.encode(animator, positive, negative)
        return positive, negative


class ControlCondition:
    def __init__(
        self,
        control_net_path: str,
        control_image_path: Optional[str]=None,
        control_image=None,
        preprocessor_fn=None,
        keyframes=[],
    ):
        self.control_net_path = control_net_path
        self.control_image_path = control_image_path
        self.control_image = control_image
        self.preprocessor_fn = preprocessor_fn
        self.keyframes = keyframes

    def encode(self, animator, positive, negative):
        if self.control_image_path is not None:
            control_image, _ = LoadImage().load_image(self.control_image_path)
        elif self.control_image is not None:
            control_image, _ = LoadPILImage().load_image(self.control_image)
        else:
            raise ValueError("No control image provided")
        if self.preprocessor_fn:
            control_image = self.preprocessor_fn(control_image)
        latent_keyframe = None
        for keyframe in self.keyframes:
            (latent_keyframe,) = LatentKeyframeNode().load_keyframe(
                keyframe["frame"],
                keyframe["strength"],
                latent_keyframe,
            )
        (timestep_keyframe,) = TimestepKeyframeNode().load_keyframe(
            start_percent=0.,
            latent_keyframe=latent_keyframe,
        )
        (control,) = ControlNetLoaderAdvanced().load_controlnet(
            control_net_path=self.control_net_path,
            timestep_keyframe=timestep_keyframe,
        )
        (positive, negative) = ControlNetApplyAdvanced().apply_controlnet(
            positive=positive,
            negative=negative,
            control_net=control,
            image=control_image,
            strength=1.,
            start_percent=0.,
            end_percent=1.,
        )
        return positive, negative
