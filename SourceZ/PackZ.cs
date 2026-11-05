using System;
using Verse;

namespace IsoRimVCEPackZ
{
    // IsoRim Waylith - Vanilla Chemfuel Expanded Pack, IsoRimZ part (loaded only with IsoRimZ: LoadFolders.xml 1.7/IsoRimZ).
    //  - Pumpjack ground only: XML (1.7/IsoRimZ/Defs/GroundOnly.xml, ProjectZ.GroundOnlyDef).
    //  - Pumpjack and floors over it: its 3D arm (top 2.29, drawn by the IsoRim part) is not in the base model IsoRimZ's height
    //    rule measures (1.08), so the pumpjack counts as too tall for a floor over it (ProjectZ.Api.RegisterHeightRule).
    //  - The refinery needs no rule: its model is taller than a storey (chimney 1.95), the height rule reads that.
    [StaticConstructorOnStartup]
    public static class PackZ
    {
        internal const string Tag = "[IsoRim VCE Pack Z] ";
        private static ThingDef pumpjack;

        static PackZ()
        {
            try
            {
                pumpjack = DefDatabase<ThingDef>.GetNamedSilentFail("VCHE_DeepchemPumpjack");
                if (pumpjack == null)
                {
                    Log.Warning(Tag + "VCHE_DeepchemPumpjack was not found: no height rule for it.");
                    return;
                }
                if (ProjectZ.Api.Version < 2)
                {
                    Log.Message(Tag + "IsoRimZ has no height rule (Api 2): floors can be built over a pumpjack.");
                    return;
                }
                RegisterRule();
            }
            catch (Exception e)
            {
                Log.Error(Tag + "Setup failed (floors can be built over a pumpjack): " + e);
            }
        }

        private static void RegisterRule()
        {
            ProjectZ.Api.RegisterHeightRule(def => def == pumpjack ? true : (bool?)null);
        }
    }
}
