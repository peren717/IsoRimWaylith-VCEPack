using System;
using System.Reflection;
using HarmonyLib;
using RimWorld;
using UnityEngine;
using Verse;

namespace IsoRimVCEPack
{
    // IsoRim Waylith - Vanilla Chemfuel Expanded Pack, IsoRim part (needs IsoRim Api 36; older: this part does nothing, logged once,
    // and the models are not added: Patches/ gates them on the same Api).
    //  - Valves: VEF's Building_PipeValve shows CompFlickable.CurrentGraphic (the _Off file while switched off). A valve switched
    //    off is in the model state "vce_valve_off"; the valves' ModelDefs draw their closed model then.
    //  - Pumpjack: VCHE's CompPumpjackAnimation.PostDraw draws the pump and the south plate with plain Graphics.DrawMesh. While
    //    the base model stands in, the pump is drawn in 3D instead: the arm at VCHE's own stroke (pumpPos), and the rod stretched
    //    from the ground up to it.
    //  - Refinery: VCHE's CompRefinery.PostDraw draws the game's fire sprite flat at the sprite's chimney. While the model stands
    //    in, it stands up as a card in the model's chimney mouth.
    // VCHE is reached by name: a missing type, field or model leaves that part as VCE draws it (logged once).
    [StaticConstructorOnStartup]
    public static class Pack
    {
        internal const string Tag = "[IsoRim VCE Pack] ";

        static Pack()
        {
            try
            {
                if (IsoRim.Api.Version < 36)
                {
                    Log.Message(Tag + "IsoRim is older than Api 36: VCE keeps IsoRim's automatic shapes.");
                    return;
                }
                Harmony h = new Harmony("peren.isorimwaylith.vcepack");
                Valves.Run();
                Pumpjack.Run(h);
                Refinery.Run(h);
            }
            catch (Exception e)
            {
                Log.Error(Tag + "Setup failed (VCE's own drawing stays in 3D): " + e);
            }
        }
    }

    internal static class Valves
    {
        internal const string Off = "vce_valve_off";
        private static ThingDef chem, deep;

        internal static void Run()
        {
            chem = DefDatabase<ThingDef>.GetNamedSilentFail("VCHE_ChemfuelValve");
            deep = DefDatabase<ThingDef>.GetNamedSilentFail("VCHE_DeepchemValve");
            IsoRim.Api.AddModelState(State);
        }

        private static string State(Thing t)
        {
            if (t.def != chem && t.def != deep)
            {
                return null;
            }
            CompFlickable flick = t.TryGetComp<CompFlickable>();
            return flick != null && !flick.SwitchIsOn ? Off : null;
        }
    }

    // The pump in 3D. VCHE moves pumpPos.z from the building's centre up 1.1 cells and back, on the map's z: up the screen in its
    // sprite. Here the same stroke lifts the arm, RiseFactor of it (user 2026-11-04: 0.75 cells at the top).
    internal static class Pumpjack
    {
        private const string ArmModel = "Models/vce_pumpjack_arm.obj";
        private const string RodModel = "Models/vce_pumpjack_rod.obj";
        private const float Rest = 0.56f;          // the arm's lowest point at rest, cells over the ground (the deck is at 0.60)
        private const float RiseFactor = 0.68f;

        private static IsoRim.ModelHandle arm, rod;
        private static AccessTools.FieldRef<object, Vector3> pumpPos;

        internal static void Run(Harmony h)
        {
            Type comp = AccessTools.TypeByName("VCHE.CompPumpjackAnimation");
            MethodInfo draw = comp != null ? AccessTools.DeclaredMethod(comp, "PostDraw") : null;
            FieldInfo field = comp != null ? AccessTools.Field(comp, "pumpPos") : null;
            if (draw == null || field == null || field.FieldType != typeof(Vector3))
            {
                Log.Warning(Pack.Tag + "VCHE's CompPumpjackAnimation (PostDraw, pumpPos) was not found: the pumpjack's pump stays as VCE draws it.");
                return;
            }
            arm = IsoRim.Api.LoadModel(ArmModel);
            rod = IsoRim.Api.LoadModel(RodModel);
            if (arm == null || rod == null)
            {
                Log.Warning(Pack.Tag + "The pumpjack's arm or rod model could not be loaded: its pump stays as VCE draws it.");
                return;
            }
            pumpPos = AccessTools.FieldRefAccess<Vector3>(comp, "pumpPos");
            h.Patch(draw, prefix: new HarmonyMethod(typeof(Pumpjack), nameof(PostDraw_Prefix)));
        }

        public static bool PostDraw_Prefix(ThingComp __instance)
        {
            Thing t = __instance.parent;
            if (t == null || !IsoRim.Api.ModelStandsIn(t))
            {
                return true;
            }
            try
            {
                Vector3 at = t.TrueCenter();
                float lift = Rest + Mathf.Max(0f, pumpPos(__instance).z - at.z) * RiseFactor;
                at.y = 0f;
                IsoRim.Api.DrawModel(rod, at, 0f, new Vector3(1f, lift, 1f), Color.white);
                at.y = lift;
                IsoRim.Api.DrawModel(arm, at, 0f, Vector3.one, Color.white);
                return false;
            }
            catch (Exception e)
            {
                Log.ErrorOnce(Pack.Tag + "Drawing the pumpjack's arm failed (VCE's sprites drawn instead): " + e, 93720001);
                return true;
            }
        }
    }

    // The refinery's fire in the model's chimney mouth (model (0, 1.85 .. 1.95, +0.72); the refinery does not rotate).
    internal static class Refinery
    {
        private const float MouthNorth = 0.72f;
        private const float CardHeight = 2.30f;    // the card's hinge: the fire sprite's middle, its foot in the mouth

        private static AccessTools.FieldRef<object, ThingComp> resource;
        private static PropertyInfo working;

        internal static void Run(Harmony h)
        {
            Type comp = AccessTools.TypeByName("VCHE.CompRefinery");
            MethodInfo draw = comp != null ? AccessTools.DeclaredMethod(comp, "PostDraw") : null;
            FieldInfo field = comp != null ? AccessTools.Field(comp, "resource") : null;
            working = field != null ? AccessTools.Property(field.FieldType, "Working") : null;
            if (draw == null || working == null || working.PropertyType != typeof(bool))
            {
                Log.Warning(Pack.Tag + "VCHE's CompRefinery (PostDraw, resource.Working) was not found: its fire stays as VCE draws it.");
                return;
            }
            resource = AccessTools.FieldRefAccess<ThingComp>(comp, "resource");
            h.Patch(draw, prefix: new HarmonyMethod(typeof(Refinery), nameof(PostDraw_Prefix)));
        }

        public static bool PostDraw_Prefix(ThingComp __instance)
        {
            Thing t = __instance.parent;
            if (t == null || !IsoRim.Api.ModelStandsIn(t))
            {
                return true;
            }
            try
            {
                if ((bool)working.GetValue(resource(__instance)))
                {
                    Vector3 at = t.TrueCenter();
                    at.z += MouthNorth;
                    using (IsoRim.Api.Upright(CardHeight, at))
                    {
                        CompFireOverlay.FireGraphic.Draw(at, Rot4.North, t, 0f);
                    }
                }
                return false;
            }
            catch (Exception e)
            {
                Log.ErrorOnce(Pack.Tag + "Drawing the refinery's fire failed (VCE's sprite drawn instead): " + e, 93720002);
                return true;
            }
        }
    }
}
